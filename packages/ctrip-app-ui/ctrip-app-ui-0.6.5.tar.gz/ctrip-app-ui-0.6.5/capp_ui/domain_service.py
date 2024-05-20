# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     domain_service.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
import time
import typing as t
from decimal import Decimal
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException, PocoTargetTimeout

from capp_ui.platforms import PlatformService
from capp_ui.config import ctrip_soft_keyboard_position
from capp_ui.mobile_terminals import stop_app, PocoProxy
from capp_ui.date_extend import is_later_than_current_time
from capp_ui.dir import get_images_dir, is_exists, join_path
from capp_ui.libs import SleepWait, LoopFindElementSubmit, logger, LoopFindElementObject, LoopExcute


class CtripAppService(object):
    """
    携程APP
    """
    IMAGE_DIR = get_images_dir()

    def __init__(self, device_id: str, port: int = 0, enable_debug: bool = False, platform: str = "Android",
                 app_name: str = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app_name = app_name or "ctrip.android.view"
        self.poco = None
        self.device = PlatformService(device_id=device_id, enable_debug=enable_debug, platform=platform,
                                      port=port).device

    def start(self) -> None:
        self.device.start_app(self.app_name)
        time.sleep(1.0)
        poco_poxy = PocoProxy()
        self.device.poco = poco_poxy.poco
        self.device.get_po = poco_poxy.get_po
        self.device.get_po_extend = poco_poxy.get_po_extend

    def stop(self) -> None:
        stop_app(self.app_name, device_id=self.device.device_id)

    def restart(self) -> bool:
        try:
            stop_app(self.app_name, device_id=self.device.device_id)
            time.sleep(1.0)
            self.device.start_app(self.app_name)
            poco_poxy = PocoProxy()
            self.device.poco = poco_poxy.poco
            self.device.get_po = poco_poxy.get_po
            self.device.get_po_extend = poco_poxy.get_po_extend
            return True
        except (Exception,):
            return False

    def hide_navigation_bar(self):
        """如果导航栏已打开，需要隐藏，导航栏很影响元素定位"""
        try:
            navigation_bar = self.device.get_po(
                type="android.widget.ImageView", name="com.android.systemui:id/hide", desc="隐藏"
            )
            navigation_bar.click()
            logger.warning("手机导航栏已被隐藏")
        except (PocoNoSuchNodeException, PocoTargetTimeout):
            logger.warning("手机没有开启导航栏")
        except Exception as e:
            logger.error("导航栏元素定位失败，error: {}".format(e))

    @LoopFindElementObject(loop=20, action="查找主页【我的】", sleep=1)
    def get_my_home(self) -> dict:
        try:
            file_name = join_path([get_images_dir(), "我的.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                # temp = (975, 2214)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            # 手机可能处于USB弹框提示点击【仅充电】
            file_name = join_path([get_images_dir(), "仅充电.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    self.device.touch(v=pos)
            else:
                # temp = (183, 1923)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            my_button = self.device.poco(
                type="android.widget.ImageView", name="ctrip.android.view:id/home_tab_bar_icon_iv"
            )
            if my_button.exists() is True:
                return {"element": my_button}
        except (Exception,):
            pass
        try:
            my_button = self.device.poco(type="android.view.ViewGroup", name="ctrip.android.view:id/a", desc="我的")
            if my_button.exists() is True:
                return {"element": my_button}
        except (Exception,):
            pass
        try:
            my_button = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", desc="我的")
            if my_button.exists() is True:
                return {"element": my_button}
        except (Exception,):
            pass
        return dict()

    def touch_element(self, attr: dict, sleep: int = 1) -> None:
        """进入app后，点击【我的】"""
        pos = attr.get("pos")
        element = attr.get("element")
        if pos:
            self.device.touch(v=pos)
        else:
            element.click()
        time.sleep(sleep)

    @LoopFindElementSubmit(loop=1, action="设置")
    def touch_settings(self):
        """我的主页，点击【设置】"""
        setting_button = self.device.poco(type="android.widget.ImageView", name="ctrip.android.view:id/a", desc="设置")
        setting_button.click()

    @LoopFindElementSubmit(loop=1, action="退出")
    def touch_logout_user(self):
        """在设置界面，点击【退出登录】"""
        self.device.quick_slide_screen(duration=1)
        logout_user = self.device.poco(
            type="android.widget.Button", name="ctrip.android.view:id/a", text="退出登录"
        )
        logout_user.click()

    @LoopFindElementSubmit(loop=1, action="确认退出")
    def touch_submit_logout(self):
        """退出登录弹框，点击【确定】"""
        logout_user = self.device.poco(
            type="android.widget.TextView", name="ctrip.android.view:id/a", text="确定"
        )
        logout_user.click()

    @LoopFindElementObject(loop=20, action="找到我的主页【待付款】", sleep=1)
    def get_todo_unpaid(self) -> dict:
        """进入my主页后，点击【待付款】"""
        try:
            file_name = join_path([get_images_dir(), "我的待办_待付款.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                # temp = (417, 947)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            # 待付款元素定位1
            unpaid_button = self.device.poco(
                type="android.widget.TextView", name="ctrip.android.view:id/a", text="待付款"
            )
            if unpaid_button.exists() is True:
                return {"element": unpaid_button}
        except (Exception,):
            pass
        try:
            # 待付款元素定位2
            unpaid_button = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="待付款"
            )
            if unpaid_button.exists() is True:
                return {"element": unpaid_button}
        except (Exception,):
            pass
        return dict()

    @LoopFindElementObject(loop=20, action="订单列表-待付款页查到【搜索】", sleep=1)
    def get_unpaid_page_search_box(self) -> dict:
        try:
            file_name = join_path([get_images_dir(), "搜索订单_搜索框.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                # temp = (289, 168)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "搜索_放大镜.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                # temp = (896, 173)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            search_box = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="搜索订单"
            )
            if search_box.exists() is True:
                return {"element": search_box}
        except (Exception,):
            pass
        return dict()

    @LoopFindElementObject(loop=20, action="搜索页查找【搜索】", sleep=1)
    def get_search_page_search_box(self) -> dict:
        try:
            search_box = self.device.poco(
                type="android.widget.EditText", name="android.widget.EditText", text="输入城市名/订单号 搜索订单"
            )
            if search_box.exists() is True:
                return {"element": search_box}
        except (Exception,):
            pass
        try:
            search_box = self.device.poco(
                type="android.widget.EditText", name="android.widget.EditText", text="输入标题关键词/订单号"
            )
            if search_box.exists() is True:
                return {"element": search_box}
        except (Exception,):
            pass
        return dict()

    def search_unpaid_order(self, attr: dict, sleep: int, ctrip_order_id: str) -> bool:
        pos = attr.get("pos")
        element = attr.get("element")
        if pos:
            self.device.touch(v=pos)
            self.device.text(text=ctrip_order_id, enter=True)
            time.sleep(sleep)
            return True
        else:
            element.click()
            search_box = self.get_search_page_search_box()
            if not search_box:
                return False
            element = search_box.get("element")
            try:
                element.click()
                element.set_text(ctrip_order_id)
                # 模拟键盘按下回车键（keyCode为66表示回车键）
                self.device.keyevent(keyname="66")
                time.sleep(sleep)
                return True
            except (Exception,):
                return False

    def get_order_status_with_order_list(self) -> str:
        """检查搜索列表界面，获取订单的状态"""
        try:
            file_name = join_path([get_images_dir(), "订单状态_待支付.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return "待支付"
            else:
                # temp = (1033, 381)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "订单状态_已出票.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return "已出票"
            else:
                # temp = (1033, 381)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "订单状态_已取消.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return "已取消"
            else:
                # temp = (1033, 381)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            unpaid_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="去支付"
            )
            if unpaid_status.exists() is True:
                return "待支付"
        except (Exception,):
            pass
        try:
            unpaid_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="待支付"
            )
            if unpaid_status.exists() is True:
                return "待支付"
        except (Exception,):
            pass
        try:
            cancel_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="已取消"
            )
            if cancel_status.exists() is True:
                return "已取消"
        except (Exception,):
            pass
        try:
            out_ticketed_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="已出票"
            )
            if out_ticketed_status.exists() is True:
                return "已出票"
        except (Exception,):
            pass
        try:
            out_ticketed_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="出票中"
            )
            if out_ticketed_status.exists() is True:
                return "出票中"
        except (Exception,):
            pass
        return ""

    @LoopFindElementObject(loop=20, action="搜索结果获取【去支付】按钮", sleep=1)
    def get_to_payment_at_list_page(self) -> dict:
        try:
            file_name = join_path([get_images_dir(), "订单状态_去支付.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                # temp = (1033, 513)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            to_payment = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", text="去支付")
            if to_payment.exists() is True:
                return {"element": to_payment}
        except (Exception,):
            pass
        return dict()

    def is_order_detail_page(self) -> bool:
        """是否在订单详情界面"""
        flag = False
        try:
            order_detail_page_1 = self.device.poco(
                type="android.widget.TextView", name="浮层标题", text="出行前必读"
            )
            if order_detail_page_1.exists() is True:
                flag = True
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        try:
            order_detail_page_2 = self.device.poco(
                type="android.widget.TextView", name="header_Text_订单详情", text="订单详情"
            )
            if order_detail_page_2.exists() is True:
                flag = True
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        try:
            order_detail_page_3 = self.device.poco(
                type="android.widget.TextView", name="operateBtnList_Text_我要退订", text="我要退订"
            )
            if order_detail_page_3.exists() is True:
                flag = True
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        try:
            order_detail_page_4 = self.device.poco(
                type="android.view.ViewGroup", name="CusHeaderView_TouchableOpacity_leftIconWrap",
                desc="CusHeaderView_TouchableOpacity_leftIconWrap"
            )
            if order_detail_page_4.exists() is True:
                flag = True
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        return flag

    @LoopFindElementObject(loop=20, action="订单详情页获取【支付金额】", sleep=1)
    def get_order_amount_with_order_detail(self) -> dict:
        try:
            amount_text = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", textMatches=r"^请在\d+:\d+前支付.*"
            )
            if amount_text.exists() is True:
                return {"element": amount_text}
        except (Exception,):
            pass
        return dict()

    def is_cancel_order(self, out_total_price: str, amount_loss_limit: str, profit_cap: str, passenger_number: int,
                        platform: str, discount_amount: str = None) -> tuple:
        """在订单详情页，判断是否需要取消订单"""
        flag = False
        remark = None
        attr = self.get_order_amount_with_order_detail()
        amount_text = attr.get("element")
        if amount_text:
            text = amount_text.get_text()
            time_match = re.search(r'(\d{2}:\d{2})', text)
            amount_match = re.search(r'¥(\d+)', text)
            if time_match and amount_match:
                time_str = time_match.group(1)
                string = "从订单获取到的过期时间为：{}".format(time_str)
                minutes = 1
                is_later = is_later_than_current_time(time_str=time_str, minutes=minutes)
                if is_later is False:
                    flag = True
                    remark = "支付时间少于{}分钟".format(minutes)
                    string = string + "，" + remark
                else:
                    amount_str = amount_match.group(1)
                    string = "从{}订单获取的支付金额：{}，劲旅订单总价：{}".format(platform, amount_str, out_total_price)
                    # 预期订单利润
                    ex_order_profit = Decimal(out_total_price) - Decimal(amount_str)
                    if discount_amount:
                        # 实际订单利润
                        ac_order_profit = ex_order_profit + Decimal(discount_amount)
                    else:
                        ac_order_profit = ex_order_profit
                    # 订单利润 < 0, 存在亏钱，与亏钱的下限进行比较
                    if ac_order_profit < 0:
                        total = Decimal(amount_loss_limit) * passenger_number
                        if ac_order_profit + total < 0:
                            flag = True
                            remark = "订单亏钱{:.2f}太多，超过订单总下限值{}(单人下限{} * {}人)".format(
                                abs(ac_order_profit), total, amount_loss_limit, passenger_number
                            )
                            logger.warning(remark)
                    # 订单利润 >= 0, 存在毛利，与利润的上限进行比较
                    else:
                        total = Decimal(profit_cap) * passenger_number
                        if ac_order_profit - total > 0:
                            flag = True
                            remark = "订单利润{:.2f}太高，超过订单总下限值{}(单人下限{} * {}人)".format(
                                ac_order_profit, total, profit_cap, passenger_number
                            )
                            logger.warning(remark)
            else:
                string = "从元素的文案<{}>提取时间与金额信息有异常".format(text)
        else:
            string = "元素定位存在异常，订单详情页没有找到订单支付金额和过期时间"
        logger.warning(string)
        return flag, remark

    @LoopFindElementObject(action="订单详情页查找【取消订单】按钮", loop=20, sleep=1)
    def get_cancel_order_with_order_detail(self) -> dict:
        try:
            file_name = join_path([get_images_dir(), "订单详情_取消订单.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            cancel_order = self.device.poco(
                type="android.widget.TextView", name="operateBtnList_Text_取消订单", text="取消订单"
            )
            if cancel_order.exists() is True:
                return {"element": cancel_order}
        except (Exception,):
            pass
        try:
            cancel_order = self.device.poco(
                type="android.view.ViewGroup", name="operateBtnList_TouchableOpacity_button",
                desc="operateBtnList_TouchableOpacity_button"
            )
            if cancel_order.exists() is True:
                return {"element": cancel_order}
        except (Exception,):
            pass
        return dict()

    @LoopFindElementObject(action="取消订单确认小弹框查找【取消订单】按钮", loop=20, sleep=1)
    def get_submit_cancel_order(self):
        try:
            file_name = join_path([get_images_dir(), "取消订单弹框_取消订单.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            cancel_order = self.device.poco(
                type="android.widget.TextView", name="Button_Text_取消订单", text="取消订单"
            )
            if cancel_order.exists() is True:
                return {"element": cancel_order}
        except (Exception,):
            pass
        return dict()

    @LoopFindElementObject(action="申请取消订单查找【申请退款】按钮", loop=20, sleep=1)
    def get_cancel_order_with_pay_refund(self) -> dict:
        try:
            file_name = join_path([get_images_dir(), "取消订单弹框_申请退票.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            pay_refund = self.device.poco(
                type="android.widget.TextView", name="NewCancelOrderLayer_Text_申请退票", text="申请退票"
            )
            if pay_refund.exists() is True:
                return {"element": pay_refund}
        except (Exception,):
            pass
        return dict()

    @LoopFindElementObject(action="申请取消订单查找【知道了】按钮", loop=20, sleep=1)
    def get_know_the_cancel_order(self):
        """确认取消后，会有一个【知道了】的小弹框"""
        try:
            file_name = join_path([get_images_dir(), "订单取消_知道了.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            submit_cancel_order = self.device.poco(
                type="android.widget.TextView", name="Button_Text_知道了", text="知道了"
            )
            if submit_cancel_order.exists() is True:
                return {"element": submit_cancel_order}
        except (Exception,):
            pass
        return dict()

    def get_order_detail_page_order_state(self) -> str:
        try:
            file_name = join_path([get_images_dir(), "订单详情.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    try:
                        file_name = join_path([get_images_dir(), "订单详情_去支付.png"])
                        if is_exists(file_name):
                            temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                            pos = self.device.exists(v=temp)
                            if pos:
                                return "去支付"
                        else:
                            # temp = (873, 440)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                            logger.warning("文件{}，没找到".format(file_name))
                    except (Exception,):
                        pass
                    try:
                        file_name = join_path([get_images_dir(), "订单详情_已取消.png"])
                        if is_exists(file_name):
                            temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                            pos = self.device.exists(v=temp)
                            if pos:
                                return "已取消"
                        else:
                            # temp = (166, 311)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                            logger.warning("文件{}，没找到".format(file_name))
                    except (Exception,):
                        pass
            else:
                # temp = (466, 173)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            order_detail = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="订单详情"
            )
            if order_detail.exists() is True:
                try:
                    canceled = self.device.poco(type="android.widget.TextView", name="android.widget.TextView",
                                                text="已取消")
                    if canceled.exists() is True:
                        return "已取消"
                except (Exception,):
                    pass
                try:
                    to_payment = self.device.poco(
                        type="android.widget.TextView", name="android.widget.TextView", text="去支付"
                    )
                    if to_payment.exists() is True:
                        return "去支付"
                except (Exception,):
                    pass
                try:
                    to_payment = self.device.poco(
                        type="android.widget.TextView", name="pcardLimit_Text_去支付", text="去支付"
                    )
                    if to_payment.exists() is True:
                        return "去支付"
                except (Exception,):
                    pass
        except (Exception,):
            pass
        return ""

    @LoopFindElementObject(loop=20, action="从订单详情页【去支付】按钮", sleep=1)
    def get_to_payment_in_order_detail(self):
        try:
            file_name = join_path([get_images_dir(), "订单详情_去支付.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return {"pos": pos}
            else:
                # temp = (873, 440)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        try:
            to_payment = self.device.poco(type="android.widget.TextView", name="pcardLimit_Text_去支付", text="去支付")
            if to_payment.exists() is True:
                return {"element": to_payment}
        except (Exception,):
            pass
        try:
            to_payment = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", text="去支付")
            if to_payment.exists() is True:
                return {"element": to_payment}
        except (Exception,):
            pass
        return dict()

    def is_need_login_with_my_page(self) -> bool:
        flag = False
        try:
            my_login = self.device.get_po(
                type="android.widget.Button", name="ctrip.android.view:id/a", text="登录/注册"
            )
            if my_login.exists() is True:
                my_login.click()
                logger.warning("手机app已经跳转至登录界面，需要做登录操作.")
                flag = True
        except (PocoNoSuchNodeException, PocoTargetTimeout):
            pass
        except Exception as e:
            logger.error(e)
        return flag

    def is_need_login_with_login_page(self) -> bool:
        flag = False
        try:
            login_page = self.device.get_po(
                type="android.widget.TextView", name="ctrip.android.view:id/a", text="手机验证码登录"
            )
            if login_page.exists() is True:
                logger.warning("手机app已经跳转至登录界面，需要做登录操作.")
                flag = True
        except (PocoNoSuchNodeException, PocoTargetTimeout):
            pass
        except Exception as e:
            logger.error(e)
        return flag

    @LoopFindElementSubmit(loop=1, action="同意服务协议")
    def select_agree_service_agreement(self):
        """选择【同意服务协议】"""
        service_agreement = self.device.get_po(
            type="android.widget.ImageView", name="ctrip.android.view:id/a", desc="勾选服务协议和个人信息保护指引"
        )
        service_agreement.click()

    @LoopFindElementSubmit(loop=1, action="账号密码登录")
    def touch_account_password_login(self):
        """选择【账号密码登录】"""
        account_password_login = self.device.get_po(
            type="android.widget.TextView", name="ctrip.android.view:id/a", text="账号密码登录"
        )
        account_password_login.click()

    @LoopFindElementSubmit(loop=1, action="输入用户名")
    def enter_account(self, username: str):
        """输入登录用户"""
        username_poco = self.device.get_po_extend(
            type="android.widget.EditText", name="android.widget.EditText", textMatches_inner=r"^\d+.*",
            global_num=0, local_num=2, touchable=True
        )[0]
        username_poco.set_text(username)

    @LoopFindElementSubmit(loop=1, action="输入密码")
    def enter_password(self, password: str):
        """输入登录密码"""
        password_poco = self.device.get_po(
            type="android.widget.EditText", name="android.widget.EditText", text="登录密码"
        )
        password_poco.set_text(password)
        self.device.quick_slide_screen(duration=0.5)

    @LoopFindElementSubmit(loop=1, action="登录")
    def touch_login(self):
        """点击【登录】"""
        login_poco = self.device.get_po(type="android.widget.TextView", name="ctrip.android.view:id/a",
                                        text="登录")
        login_poco.click()

    @SleepWait(wait_time=1)
    def touch_payment_method(self) -> None:
        """点击【换卡支付，支持境外卡】"""
        try:
            payment_method = self.device.get_po(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="换卡支付，支持境外卡"
            )
            payment_method.click()
            logger.info("在安全收银台界面，点击选择【换卡支付，支持境外卡】")
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有出现收银台，可以直接选择银行卡支付.")

    @SleepWait(wait_time=1)
    def select_payment_method(self, payment_method: str) -> None:
        """选择【xxxy银行储蓄卡(xxxx)】"""
        try:
            method = self.device.get_po(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text=payment_method
            )
            method.click()
            logger.info("点击选择【{}】".format(payment_method))
        except (Exception,):
            pass

    # @LoopFindElementObject(action="检测点击详情页去支付后，是否出现机舱售罄小弹框", loop=1, sleep=1)
    def get_sold_out_with_after_to_payment(self) -> dict:
        # 1. 图像识别方式检测是否出现航班售罄小弹框
        try:
            file_name = join_path([get_images_dir(), "订单详情_舱位售完.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    logger.warning("图像识别方式检测到有小弹框【价格舱位已售罄】")
                    return {"pos": pos}
        except (Exception,):
            pass
        # 2. 元素定位方式检测是否出现航班售罄小弹框
        try:
            sold_out = self.device.get_po(
                type="android.widget.TextView", name="Button_Text_知道了", text="知道了"
            )
            if sold_out.exists() is True:
                logger.warning("元素定位方式检测到有小弹框【价格舱位已售罄】")
                return {"element": sold_out}
        except (Exception,):
            pass
        return dict()

    # @LoopFindElementObject(action="检测点击详情页去支付后，是否出现行程冲突小弹框", loop=1, sleep=1)
    def get_itinerary_conflict_with_after_to_payment(self) -> dict:
        # 1. 图像识别方式检测是否出现行程冲突小弹框
        try:
            file_name = join_path([get_images_dir(), "订单详情_行程冲突.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    logger.warning("图像识别方式检测到有小弹框【行程冲突】，需要点击【继续支付】")
                    return {"pos": pos}
        except (Exception,):
            pass
        # 2. 元素定位方式检测是否出现行程冲突小弹框
        try:
            itinerary_conflict = self.device.get_po(
                type="android.widget.TextView", name="Button_Text_继续支付", text="继续支付"
            )
            if itinerary_conflict.exists() is True:
                logger.warning("元素定位方式检测到有小弹框【行程冲突】，需要点击【继续支付】")
                return {"element": itinerary_conflict}
        except (Exception,):
            pass
        return dict()

    def get_more_payment(self) -> dict:
        # 1. 检测到小弹框， 图像识别定位特征是：【更多付款方式】
        try:
            file_name = join_path([get_images_dir(), "更多付款方式.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    # logger.warning("图像识别方式检测到有小弹框，需要点击【更多付款方式】")
                    return {"pos": pos}
        except (Exception,):
            pass
        # 2. 检测到小弹框， 元素定位方式特征是：【更多付款方式】
        try:
            more_payment_type = self.device.get_po(
                type="android.view.ViewGroup ", name="更多付款方式", desc="更多付款方式"
            )
            if more_payment_type.exists() is True:
                # logger.warning("元素定位方式检测到有小弹框，需要点击【更多付款方式】")
                return {"element": more_payment_type}
        except (Exception,):
            pass
        return dict()

    def get_safe_cash(self) -> dict:
        # 1. 检测到小弹框， 图像识别定位特征是：【更多付款方式】
        try:
            file_name = join_path([get_images_dir(), "安全收银台.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    # logger.warning("图像识别方式检测到页面已经进入安全收银台")
                    return {"pos": pos}
        except (Exception,):
            pass
        # 2. 检测到小弹框， 元素定位方式特征是：【安全收银台】
        try:
            safe_cash = self.device.get_po(
                type="android.widget.TextView", name="android.widget.TextView", text="安全收银台"
            )
            if safe_cash.exists() is True:
                # logger.warning("元素定位方式检测到页面已经进入安全收银台")
                return {"element": safe_cash}
        except (Exception,):
            pass
        return dict()

    def get_preferential_popup(self) -> dict:
        # 1. 检测到小弹框， 图像识别定位特征是：【关闭】
        try:
            file_name = join_path([get_images_dir(), "安全收银台_优惠关闭.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    logger.warning("图像识别方式检测到页面弹出优惠小窗口，点击【关闭】")
                    return {"pos": pos}
        except (Exception,):
            pass
        # 2. 检测到小弹框， 元素定位方式特征是：【安全收银台】
        try:
            preferential_popup = self.device.get_po(
                type="android.widget.TextView", name="android.widget.TextView", text="关闭"
            )
            if preferential_popup.exists() is True:
                logger.warning("元素定位方式检测到页面弹出优惠小窗口，点击【关闭】")
                return {"element": preferential_popup}
        except (Exception,):
            pass
        return dict()

    def __get_wallet_element(self) -> UIObjectProxy:
        return self.device.get_po(
            type="android.widget.TextView", name="android.widget.TextView", textMatches=r'^钱包.*'
        )

    @SleepWait(wait_time=1)
    def is_wallet_usable(self) -> t.Tuple:
        """
        判断收银台界面，钱包支付是否可用，如果可用，还要判断钱包的余额是否够用
        """
        flag = False
        amount = 0.00
        try:
            wallet = self.__get_wallet_element()
            if wallet.exists() is True:
                logger.info("账户钱包没有隐藏，可以选中.")
                text = wallet.get_text().strip("")
                logger.info("账户钱包可用余额的展示为：{}.".format(text))
                pattern = r'\d+\.\d+'
                # 使用 re.findall() 函数查找字符串中匹配的浮点数
                matches = re.findall(pattern, text)
                # 如果找到了匹配的浮点数，则返回第一个匹配结果（应该只有一个）
                if matches:
                    flag, amount = True, Decimal(matches[0])
                else:
                    logger.warning("提取钱包余额<{}>有异常，钱包为不可用状态，将选择银行卡支付".format(text))
            else:
                logger.info("账户钱包被隐藏了，不能操作钱包.")
        except (PocoNoSuchNodeException, Exception):
            logger.warning("安全收银台界面，没有出现钱包的选择入口.")
        return flag, amount

    def touch_wallet_payment(self) -> None:
        try:
            wallet = self.__get_wallet_element()
            wallet.click()
            time.sleep(1)
        except (Exception,):
            pass

    def select_gift_card(self, payment_method: str) -> None:
        """选择对应的礼品卡"""
        try:
            gift_card = self.device.get_po(
                type="android.widget.TextView", name="android.widget.TextView", text=payment_method
            )
            gift_card.click()
            time.sleep(1)
        except (Exception,):
            pass

    def get_gift_card_deduction_amount(self) -> str:
        """获取礼品卡抵扣金额"""
        value = ""
        try:
            gift_card = self.device.get_po(
                type="android.widget.TextView", name="android.widget.TextView", textMatches=r"^使用.*"
            )
            text_value = gift_card.get_text()
            pattern = r'¥(\d+(\.\d+)?)'
            matches = re.findall(pattern, text_value)
            if len(matches) > 0:
                value = matches[0][0]
                # logger.warning("当前礼品卡抵扣金额为：{}".format(value))
            else:
                logger.warning("获取到的礼品卡抵扣金额文案未：{}".format(text_value))
        except (Exception,):
            logger.error("获取礼品卡抵扣金额出现异常")
        return value

    def touch_wallet_immediate_payment(self) -> None:
        """选择对应的礼品卡，点击【使用钱包全额抵扣，立即支付】"""
        try:
            wallet_immediate_payment = self.device.get_po(
                type="android.widget.TextView", name="android.widget.TextView", text="使用钱包全额抵扣，立即支付"
            )
            wallet_immediate_payment.click()
            time.sleep(1)
        except (Exception,):
            pass

    @SleepWait(wait_time=1)
    def select_point_deduction(self) -> None:
        """
        支付界面，选择【积分抵扣】，这里的逻辑是，如果已经选中，再点击积分抵扣，就会变成取消抵扣
        """
        default_text = "100积分抵扣1元"
        selected_text = "-¥10.00"
        poco = None
        try:
            point_deduction = self.device.get_po(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text=selected_text
            )
            if point_deduction.exists():
                poco = point_deduction
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有找到已选中积分抵扣，可能它是初始状态，还未选择.")
        if poco is None:
            try:
                poco = self.device.get_po(
                    type="android.widget.TextView",
                    name="android.widget.TextView",
                    text=default_text
                )
                if poco.exists():
                    poco.click()
                    logger.info("积分抵扣已经选中，接下来将进行支付操作.")
            except (PocoNoSuchNodeException, Exception):
                logger.warning("既没有找到默认的积分抵扣选项，也没有找到已选中的积分抵扣.")
        else:
            logger.info("积分抵扣已经选中，接下来将进行支付操作.")

    def touch_bank_card_payment(self) -> None:
        """
        支付界面，选择【银行卡支付】
        """
        try:
            point_deduction = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="银行卡支付",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            point_deduction.click()
            time.sleep(1)
        except (Exception,):
            pass

    def get_ticket_actual_amount(self) -> Decimal:
        """
        确定使用积分抵扣后，票据的实际支付金额
        """
        actual_amount = Decimal("9999999999.9999999999")
        try:
            ticket_actual_amount = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                textMatches_inner=r"^¥\d+.\d*",
                global_num=0,
                local_num=2,
                touchable=False,
            )[0]
            actual_amount = ticket_actual_amount.get_text()
            actual_amount = Decimal(actual_amount[1:]) if actual_amount and isinstance(
                actual_amount, str) else Decimal("9999999999.9999999999")
        except (Exception,):
            pass
        return actual_amount

    def get_ticket_deduction_amount(self) -> Decimal:
        """
        使用积分抵扣的金额
        """
        deduction_amount = Decimal("-9999999999.9999999999")
        try:
            tickect_deduction_amount = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                textMatches_inner=r"^-¥\d+.\d*",
                global_num=0,
                local_num=4,
                touchable=False,
            )[0]
            deduction_amount = tickect_deduction_amount.get_text()
            deduction_amount = Decimal(deduction_amount[2:]) if deduction_amount and isinstance(
                deduction_amount, str) else Decimal("-9999999999.9999999999")
        except (Exception,):
            pass
        return deduction_amount

    @SleepWait(wait_time=8)
    def enter_payment_pass(self, payment_pass: str, device_id: str, enable_debug: bool = False, port: int = 0,
                           platform: str = "Android") -> None:
        """
        请输入支付密码
        """
        device = PlatformService.minicap_device(
            device_id=device_id, enable_debug=enable_debug, platform=platform, port=port
        )
        payment_pass = payment_pass if isinstance(payment_pass, str) else str(payment_pass)
        for char in payment_pass:
            file_name = join_path([get_images_dir(), "支付_{}.png".format(char)])
            if is_exists(file_name):
                temp = device.get_cv_template(file_name=file_name)
                device.touch(v=temp)
            else:
                raise ValueError("文件<{}>缺失...", format(file_name))

    @SleepWait(wait_time=8)
    def enter_payment_pass_by_position(self, payment_pass: str) -> None:
        """
        请输入支付密码
        """
        try:
            payment_pass = payment_pass if isinstance(payment_pass, str) else str(payment_pass)
            for char in payment_pass:
                char_position = ctrip_soft_keyboard_position.get(char)
                self.device.touch(v=char_position)
        except (Exception,):
            pass

    @SleepWait(wait_time=1)
    def is_balance(self, payment_card: str) -> bool:
        """
        判断是否出现余额不足的小弹框
        """
        flag = False
        try:
            balance_poco = self.device.get_po(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="更换支付方式"
            )
            if balance_poco.exists():
                logger.warning("银行卡【{}】余额不足，请更换其他银行卡或使用其他支付方式.".format(payment_card))
                balance_poco.click()
                flag = True
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有找到余额不足小弹框，接下来更换支付方式，继续支付.")
        return flag

    @SleepWait(wait_time=1)
    def is_payment_complete(self) -> bool:
        """
        判断是否限额，余额不足或其他异常，没有异常的话，输入密码后，会出现【完成】小弹框界面
        """
        flag = False
        try:
            limit_quotas = self.device.poco(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="完成"
            )
            if limit_quotas.exists():
                # logger.warning("银行卡支付成功，等待出票.")
                flag = True
        except (PocoNoSuchNodeException, Exception):
            logger.warning("银行卡支付有异常，需要更新支付类型，重新支付.")
        return flag

    def get_order_with_payment_amount(self) -> Decimal:
        """获取支付成功后的订单金额"""
        payment_amount = Decimal(-9999999999.9999999999)
        try:
            payment_amount = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                textMatches_inner=r"^\d+.\d*",
                global_num=0,
                local_num=5,
                touchable=False,
            )[0]
            payment_amount = payment_amount.get_text()
            logger.info("从支付成功界面获取到的实际支付金额是: {}".format(payment_amount))
            payment_amount = Decimal(payment_amount) if payment_amount and isinstance(
                payment_amount, str) else Decimal(-9999999999.9999999999)
        except Exception as e:
            logger.error(str(e))
        return payment_amount

    @LoopFindElementSubmit(loop=3, action="支付完成")
    def touch_payment_complete(self):
        """在支付成功界面，点击【完成】"""
        try:
            payment_complete_button = self.device.poco(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="完成"
            )
            payment_complete_button.click()
            logger.warning("点击支付成功界面的【完成】按钮.")
        except (Exception,):
            pass

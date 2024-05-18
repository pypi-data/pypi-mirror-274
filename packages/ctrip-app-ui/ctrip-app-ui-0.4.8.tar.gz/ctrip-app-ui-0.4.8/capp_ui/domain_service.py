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
from capp_ui.utils import get_ui_object_proxy_attr
from capp_ui.config import ctrip_soft_keyboard_position
from capp_ui.mobile_terminals import stop_app, PocoProxy
from capp_ui.date_extend import is_later_than_current_time
from capp_ui.dir import get_images_dir, is_exists, join_path
from capp_ui.date_extend import get_trip_year_month_day, get_datetime_area, is_public_holiday
from capp_ui.libs import SleepWait, LoopFindElement, LoopFindElementSubmit, logger, LoopExcute


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

    def restart(self):
        stop_app(self.app_name, device_id=self.device.device_id)
        time.sleep(1.0)
        self.device.start_app(self.app_name)
        poco_poxy = PocoProxy()
        self.device.poco = poco_poxy.poco
        self.device.get_po = poco_poxy.get_po
        self.device.get_po_extend = poco_poxy.get_po_extend

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

    @LoopFindElementSubmit(loop=3, action="首页")
    def touch_home(self):
        """进入app后，点击【首页】"""
        file_name = join_path([get_images_dir(), "首页.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (154, 2878)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @LoopExcute(loop=20, action="点击【我的】", sleep=1)
    def touch_my(self) -> bool:
        """进入app后，点击【我的】"""
        try:
            my_button = self.device.poco(
                type="android.widget.ImageView", name="ctrip.android.view:id/home_tab_bar_icon_iv"
            )
            if my_button.exists() is True:
                my_button.click()
                time.sleep(0.5)
                my_button = self.device.poco(
                    type="android.widget.ImageView", name="ctrip.android.view:id/home_tab_bar_icon_iv"
                )
                if my_button.exists() is False:
                    return True
        except (Exception,):
            pass
        try:

            my_button = self.device.poco(type="android.view.ViewGroup", name="ctrip.android.view:id/a", desc="我的")
            if my_button.exists() is True:
                my_button.click()
                time.sleep(0.5)
                my_button = self.device.poco(type="android.view.ViewGroup", name="ctrip.android.view:id/a", desc="我的")
                if my_button.exists() is False:
                    return True
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "我的.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    self.device.touch(v=pos)
                    time.sleep(0.5)
                    pos = self.device.exists(v=temp)
                    if pos is False:
                        return True
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
                # temp = (975, 2214)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        return False

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

    @LoopExcute(loop=20, action="点击【待付款】", sleep=1)
    def touch_unpaid(self) -> bool:
        """进入my主页后，点击【待付款】"""
        try:
            # 待付款元素定位1
            unpaid_button = self.device.poco(
                type="android.widget.TextView", name="ctrip.android.view:id/a", text="待付款"
            )
            if unpaid_button.exists() is True:
                unpaid_button.click()
                time.sleep(0.5)
                unpaid_button = self.device.poco(
                    type="android.widget.TextView", name="ctrip.android.view:id/a", text="待付款"
                )
                if unpaid_button.exists() is False:
                    return True
        except (Exception,):
            pass
        try:
            # 待付款元素定位2
            unpaid_button = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="待付款"
            )
            if unpaid_button.exists() is True:
                unpaid_button.click()
                time.sleep(0.5)
                unpaid_button = self.device.poco(
                    type="android.widget.TextView", name="android.widget.TextView", text="待付款"
                )
                if unpaid_button.exists() is False:
                    return True
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "我的待办_待付款.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    self.device.touch(v=pos)
                    time.sleep(0.5)
                    pos = self.device.exists(v=temp)
                    if pos is False:
                        return True
            else:
                # temp = (417, 947)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        return False

    @LoopExcute(loop=20, action="搜索【待支付订单】", sleep=1)
    def search_unpaid_order(self, ctrip_order_id: str) -> bool:
        """搜索待支付的订单，这里面有2个步骤：1，定位搜索入口，并点击进入搜索界面，2.输入搜索内容"""
        try:
            search_box = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="搜索订单"
            )
            if search_box.exists() is True:
                search_box.click()
                time.sleep(0.5)
                search_box = self.device.poco(
                    type="android.widget.EditText", name="android.widget.EditText", text="输入城市名/订单号 搜索订单"
                )
                if search_box.exists() is True:
                    search_box.click()
                    search_box.set_text(ctrip_order_id)
                    # 模拟键盘按下回车键（keyCode为66表示回车键）
                    self.device.keyevent(keyname="66")
                    time.sleep(1)
                    return True
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "搜索订单_搜索框.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    self.device.touch(v=pos)
                    time.sleep(0.5)
                    pos = self.device.exists(v=temp)
                    if pos is False:
                        self.device.text(text=ctrip_order_id, enter=True)
                        time.sleep(1)
                        return True
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
                    self.device.touch(v=pos)
                    time.sleep(0.5)
                    pos = self.device.exists(v=temp)
                    if pos is False:
                        self.device.text(text=ctrip_order_id, enter=True)
                        time.sleep(1)
                        return True
            else:
                # temp = (896, 173)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        return False

    @LoopFindElementSubmit(loop=3, action="列表页搜索框")
    def touch_list_page_search_box(self):
        """进入待付款列表页，点击【搜索框】"""
        search_box = self.device.poco(
            type="android.widget.TextView", name="android.widget.TextView", text="搜索订单"
        )
        search_box.click()

    @LoopFindElementSubmit(loop=3, action="搜索页搜索框")
    def touch_search_page_search_box(self, ctrip_order_id: str):
        """进入搜索页，点击【搜索框】"""
        search_box = self.device.poco(
            type="android.widget.EditText", name="android.widget.EditText", text="输入城市名/订单号 搜索订单"
        )
        search_box.click()
        search_box.set_text(ctrip_order_id)
        # 模拟键盘按下回车键（keyCode为66表示回车键）
        self.device.keyevent(keyname="66")

    @LoopExcute(loop=1, action="判断订单是否为【待支付】", sleep=1)
    def is_exist_to_payment_at_list_page(self) -> bool:
        """检查搜索列表界面，是否存在【待支付】状态"""
        try:
            is_exist = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", text="去支付")
            if is_exist.exists() is True:
                return True
        except (Exception,):
            pass
        try:
            is_exist = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", text="待支付")
            if is_exist.exists() is True:
                return True
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "订单状态_待支付.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    return True
            else:
                # temp = (1033, 381)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        return False

    def get_order_status(self) -> str:
        """检查搜索列表界面，获取订单的状态"""
        status = None
        try:
            unpaid_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="去支付"
            )
            if unpaid_status.exists() is True:
                status = "待支付"
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        try:
            cancel_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="已取消"
            )
            if cancel_status.exists() is True:
                status = "已取消"
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        try:
            out_ticketed_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="已出票"
            )
            if out_ticketed_status.exists() is True:
                status = "已出票"
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        try:
            out_ticketed_status = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", text="出票中"
            )
            if out_ticketed_status.exists() is True:
                status = "出票中"
        except (PocoNoSuchNodeException, PocoTargetTimeout, Exception):
            pass
        return status

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

    @SleepWait(wait_time=1)
    def touch_go_back_to_unpaid_list_page_by_search_page(self) -> None:
        """从搜索界面退回到【待支付】列表页"""
        try:
            go_back = self.device.poco(type="android.widget.TextView", name="icon_back")
            if go_back.exists() is True:
                go_back.click()
                go_back.click()
        except (PocoNoSuchNodeException, PocoTargetTimeout):
            pass
        except Exception as e:
            logger.error(e)

    @SleepWait(wait_time=1)
    def touch_go_back_to_search_page_page_by_cancel_page(self) -> None:
        """从订单撤销页返回到订单待支付列表页"""
        try:
            go_back = self.device.poco(
                type="android.view.ViewGroup", name="CusHeaderView_TouchableOpacity_leftIconWrap",
                desc="CusHeaderView_TouchableOpacity_leftIconWrap"
            )
            if go_back.exists() is True:
                go_back.click()
        except (PocoNoSuchNodeException, PocoTargetTimeout):
            pass
        except Exception as e:
            logger.error(e)

    @LoopExcute(loop=3, sleep=1, action="点击【去支付】")
    def touch_to_payment_at_list_page(self) -> bool:
        """进入待付款列表页，点击【去支付】"""
        try:
            to_payment = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", text="去支付")
            if to_payment.exists() is True:
                to_payment.click()
                time.sleep(0.5)
                to_payment = self.device.poco(
                    type="android.widget.TextView", name="android.widget.TextView", text="去支付"
                )
                if to_payment.exists() is False:
                    return True
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "订单状态_待支付.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    self.device.touch(v=pos)
                    time.sleep(0.5)
                    pos = self.device.exists(v=temp)
                    if pos is False:
                        return True
            else:
                # temp = (1033, 513)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass
        return False

    @SleepWait(wait_time=1)
    def is_cancel_order(self, out_total_price: str, amount_loss_limit: str, profit_cap: str, passenger_number: int,
                        discount_amount: str = None) -> tuple:
        """在订单详情页，判断是否需要取消订单"""
        flag = False
        remark = None
        try:
            is_cancel = self.device.poco(
                type="android.widget.TextView", name="android.widget.TextView", textMatches=r"^请在\d+:\d+前支付.*"
            )
            if is_cancel.exists() is True:
                text = is_cancel.get_text()
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
                        string = "从携程订单获取的支付金额：{}，劲旅订单总价：{}".format(amount_str, out_total_price)
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
        except (PocoNoSuchNodeException, PocoTargetTimeout):
            pass
        except Exception as e:
            logger.error(e)
        return flag, remark

    @LoopFindElementSubmit(loop=1, action="取消订单")
    def touch_cancel_order(self):
        cancel_order = self.device.poco(
            type="android.widget.TextView", name="operateBtnList_Text_取消订单", text="取消订单"
        )
        cancel_order.click()

    @LoopFindElementSubmit(loop=1, action="确认取消订单")
    def touch_submit_cancel_order(self):
        """再次确认是否要取消订单"""
        submit_cancel_order = self.device.poco(
            type="android.widget.TextView", name="Button_Text_取消订单", text="取消订单"
        )
        submit_cancel_order.click()

    @LoopFindElementSubmit(loop=1, action="知道了")
    def touch_know_the_cancel_order(self):
        """确认取消后，会有一个【知道了】的小弹框"""
        submit_cancel_order = self.device.poco(
            type="android.widget.TextView", name="Button_Text_知道了", text="知道了"
        )
        submit_cancel_order.click()

    def get_order_detail_page_order_state(self) -> str:
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
        return ""

    @LoopExcute(action="订单详情页点击【去支付】", loop=10, sleep=1)
    def touch_to_payment_at_order_detail(self):
        """在订单详情页，点击【去支付】"""
        try:
            to_payment = self.device.poco(type="android.widget.TextView", name="pcardLimit_Text_去支付", text="去支付")
            if to_payment.exists() is True:
                to_payment.click()
                time.sleep(3)
                to_payment = self.device.poco(
                    type="android.widget.TextView", name="pcardLimit_Text_去支付", text="去支付"
                )
                if to_payment.exists() is False:
                    return True
        except (Exception,):
            pass
        try:
            to_payment = self.device.poco(type="android.widget.TextView", name="android.widget.TextView", text="去支付")
            if to_payment.exists() is True:
                to_payment.click()
                time.sleep(3)
                to_payment = self.device.poco(
                    type="android.widget.TextView", name="android.widget.TextView", text="去支付"
                )
                if to_payment.exists() is False:
                    return True
        except (Exception,):
            pass
        try:
            file_name = join_path([get_images_dir(), "订单详情_去支付.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name, threshold=0.9)
                pos = self.device.exists(v=temp)
                if pos:
                    self.device.touch(v=pos)
                    time.sleep(3)
                    pos = self.device.exists(v=temp)
                    if pos is False:
                        return True
            else:
                # temp = (873, 440)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                logger.warning("文件{}，没找到".format(file_name))
        except (Exception,):
            pass

    @SleepWait(wait_time=1)
    def touch_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】"""
        file_name = join_path([get_images_dir(), "机票.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (445, 560)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_special_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】，点击【特价机票】"""
        file_name = join_path([get_images_dir(), "特价机票.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (517, 592)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def select_departure_city(self) -> None:
        departure_city = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner=r"\S+",
            global_num=0,
            local_num=2,
        )[0]
        departure_city.click()

    @SleepWait(wait_time=3)
    def enter_search_value(self, search_value: str) -> None:
        search_box = self.device.poco(type="android.widget.EditText")
        search_box.click()
        search_box.set_text(search_value)

    @SleepWait(wait_time=5)
    def select_search_result_first_city(self, select_value: str):
        search_result = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner=".* {} .*".format(select_value),
            global_num=0,
            local_num=2,
            touchable=False
        )[0]
        value = search_result.get_text().strip()
        search_result.click()
        logger.info("从搜索结果中，选择<{}>这条数据.".format(value))

    @SleepWait(wait_time=3)
    def sumbit_search_result(self):
        """选择城市后，需要点击【确认】按钮"""
        """
        file_name = join_path([get_images_dir(), "搜索确认.png"])
        if is_exists(file_name):
            template = self.device.get_cv_template(file_name=file_name)
            result = self.device.find_all(v=template)
            temp = result[0].get("result")
        else:
            temp = (1273, 624) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.adb_touch(v=temp)
        """
        search_result = self.device.get_po_extend(
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="确认",
            global_num=0,
            local_num=2,
            touchable=True,
        )[0]
        search_result.click()

    @SleepWait(wait_time=1)
    def select_arrive_city(self) -> None:
        arrive_city = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner=r"\S+",
            global_num=0,
            local_num=4,
        )[0]
        arrive_city.click()

    @SleepWait(wait_time=1)
    def select_trip_date(self) -> None:
        trip_date = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            textMatches_inner="^出发.*",
            global_num=0,
            local_num=9,
        )[0]
        trip_date.click()

    @SleepWait(wait_time=1)
    def select_trip_expect_month(self, date_str: str) -> None:
        _, trip_month, _ = get_trip_year_month_day(date_str=date_str)
        top_month_area = self.device.get_po_extend(
            type="android.widget.TextView",
            name="ctrip.android.view:id/a",
            text=trip_month,
            touchable=False,
            global_num=0,
            local_num=2,
        )[0]
        top_month_area.click()

    @SleepWait(wait_time=2)
    def select_trip_expect_day(self, date_str: str) -> None:
        _, _, trip_day = get_trip_year_month_day(date_str=date_str)
        day_str = "{}_red".format(trip_day) if is_public_holiday(
            date_str=date_str) else "{}_blue".format(trip_day)
        file_name = join_path([get_images_dir(), "{}.png".format(day_str)])
        logger.info("需要识别日历中的日期文件是：{}".format(file_name))
        if is_exists(file_name):
            # threshold 提高识别灵敏度，灵敏度太低，容易将相似的结果匹配出来
            temp = self.device.get_cv_template(
                file_name=file_name, threshold=0.9)
            find_results = self.device.find_all(v=temp)
            if isinstance(find_results, t.List) and len(find_results) > 0:
                sorted_list = sorted(find_results, key=lambda x: (
                    x['result'][1], x['result'][0]))
                temp = sorted_list[0].get("result")
            else:
                raise ValueError(
                    "According to the image file <{}>, no corresponding element was found".format(file_name))
        else:
            raise ValueError("<{}> file does not exist".format(file_name))
        self.device.touch(v=temp)

    @SleepWait(wait_time=1)
    def touch_only_query_some_day(self) -> None:
        """
        点击 【预计出发日期】 界面的 【仅查询当天】 按钮
        """
        only_query_some_day = self.device.get_po_extend(
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="仅查询当天",
            global_num=0,
            local_num=5,
        )[0]
        only_query_some_day.click()

    @SleepWait(wait_time=8)
    def touch_query_special(self) -> None:
        """
        特价机票界面，点击【查询特价】
        """
        query_special_flight = self.device.get_po_extend(
            type="android.widget.Button",
            name="ctrip.android.view:id/a",
            text="查询特价",
            global_num=0,
            local_num=5,
            touchable=True,
        )[0]
        query_special_flight.click()

    def is_exist_flight_in_screen(self, flight: str) -> bool:
        """
        检索需要购买的航班是否出现在初始的屏幕中
        """
        logger.info("判断航班<{}>机票信息是否在初始列表当中...".format(flight))
        in_screen = self.device.get_po(
            type="android.widget.TextView", name="第{}航班航司信息".format(flight))
        if in_screen.exists():
            return True
        else:
            return False

    def touch_flight_inland_single_list_filter(self) -> None:
        po = self.device.get_po(type="android.widget.TextView", name="筛选")
        if po.exists():
            # 说明筛选入口在底部
            logger.info("查询到的航班数量不多，筛选的按钮在UI的底部。")
            self.__touch_flight_inland_single_list_bottom_filter()
        else:
            self.__touch_flight_inland_single_list_top_filter()

    @SleepWait(wait_time=1)
    def touch_clear_filter(self) -> None:
        """
        点击【清空】，防止缓存数据，干扰配置过滤条件，当然需要判断，【清空】按钮，是否为激活状态，未激活的情况下，按钮是灰色，无法点击
        """
        clear_button = self.device.get_po(
            type="android.view.ViewGroup", name="筛选清空按钮"
        )[0]
        clear_button_attr = get_ui_object_proxy_attr(
            ui_object_proxy=clear_button)
        is_enabled = clear_button_attr.get("enabled")
        if is_enabled is True:
            clear_text = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="清空",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            clear_text.click()

    @SleepWait(wait_time=1)
    def __touch_flight_inland_single_list_top_filter(self) -> None:
        """
        航线特价机票查询列表，点击顶部的【筛选】
        """
        filter1 = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="筛选",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        filter1.click()

    @SleepWait(wait_time=1)
    def __touch_flight_inland_single_list_bottom_filter(self) -> None:
        """
        航线特价机票查询列表，点击底部的【筛选】
        """
        filter1 = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选",
            text="筛选",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        filter1.click()

    @SleepWait(wait_time=1)
    def touch_filter_departure_time(self) -> None:
        """
        航班列表底部的筛选界面，点击【起飞时间】
        """
        departure_time = self.device.get_po_extend(
            type="android.widget.TextView",
            name="起飞时间",
            text="起飞时间",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        departure_time.click()

    @SleepWait(wait_time=1)
    def select_filter_departure_time_area(self, date_str: str) -> None:
        """
        选择筛选条件中的起飞时间区域，00:00~06:00,06:00~12:00,12:00~18:00,18:00~24:00
        """
        time_area_str = get_datetime_area(date_str=date_str)
        time_area = self.device.get_po_extend(
            type="android.widget.TextView",
            # name="{}筛选控件".format(time_area_str),
            text=time_area_str,
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        time_area.click()

    @SleepWait(wait_time=1)
    def touch_filter_airline(self) -> None:
        """
        航班列表底部的筛选界面，点击【航空公司】
        """
        airline = self.device.get_po_extend(
            type="android.widget.TextView",
            name="航空公司",
            text="航空公司",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        airline.click()

    @SleepWait(wait_time=1)
    def select_filter_airline_company(self, ac: str) -> None:
        """
        选择筛选条件中的航空公司
        """
        airline_company = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选按钮{}".format(ac),
            text=ac,
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        airline_company.click()

    @SleepWait(wait_time=8)
    def touch_filter_submit_button(self) -> None:
        """
        确认筛选条件
        """
        submit_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="筛选确定按钮文案",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        submit_button.click()

    @SleepWait(wait_time=5)
    def select_special_flight(self, flight: str) -> None:
        """
        从特价机票列表中选择本次订单的航班
        """
        desc = "第{}航班航司信息".format(flight)
        special_flight = self.device.get_po(
            type="android.widget.TextView", name=desc)
        if special_flight.exists():
            abs_position = self.device.get_abs_position(element=special_flight)
            # special_flight.click()
            logger.info("选择：{}".format(desc))
            self.device.touch((abs_position[0], abs_position[1] - 200))
        else:
            raise ValueError("当前页面没有找到", desc)

    @SleepWait(wait_time=1)
    def get_special_flight_amount(self) -> Decimal:
        """
        检索航班经济舱的第二条数据的金额
        """
        lowerest_amount_po = self.device.get_po(
            type="android.widget.TextView", name="第2个政策成人价格金额"
        )[0]
        ui_object_proxy_attr = get_ui_object_proxy_attr(
            ui_object_proxy=lowerest_amount_po)
        text = ui_object_proxy_attr.get("text")
        logger.info("获取到的机票最低价为：{}".format(text))
        # 9999999999.9999999999 表示金额无限大，仅限于作为后续的比较逻辑默认值
        return Decimal(text) if isinstance(text, str) and text.isdigit() else 9999999999.9999999999

    def is_direct_booking(self) -> True:
        """
        在经济舱航班列表中，存在某些航班，没有【选购】按钮，点击【订】直接进入下单界面，相当于少了一次点击
        """
        booking = self.device.get_po(
            type="android.widget.TextView", name="btn_book_2预订按钮", text="订")
        if booking.exists():
            return True
        else:
            return False

    @SleepWait(wait_time=1)
    def touch_direct_booking_button(self) -> None:
        """
        在经济舱航班列表中，存在某些航班，点击【订】直接进入下单界面
        """
        direct_booking_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="btn_book_2预订按钮",
            text="订",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        direct_booking_button.click()

    @SleepWait(wait_time=1)
    def touch_booking_the_second_button(self) -> None:
        """
        点击航班经济舱第二条数据中的【选购】
        """
        the_second_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="drop_book_2预订按钮",
            text="选购",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        the_second_button.click()

    @SleepWait(wait_time=5)
    def touch_ordinary_booking_button(self) -> None:
        """
        点击航班经济舱第二条数据中的【普通预订】
        """
        ordinary_booking_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="第2个政策选购第7个X产品预订按钮",
            text="订",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        ordinary_booking_button.click()

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

    @LoopFindElement(loop=5)
    # @SleepWait(wait_time=3)
    def touch_more_passengers_button(self) -> None:
        """
        点击【更多乘机人】按钮
        """
        add_passenger_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="新增乘机人按钮icon",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        add_passenger_button.click()

    @LoopFindElement(loop=5)
    # @SleepWait(wait_time=1)
    def touch_add_passengers_button(self) -> None:
        """
        点击【新增乘机人】按钮
        """
        add_passenger_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="乘机人列表新增乘机人文案",
            text="新增乘机人",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        add_passenger_button.click()

    @SleepWait(wait_time=1)
    def enter_passenger_username(self, passenger: str) -> None:
        """
        录入乘客姓名
        """
        passenger_username = self.device.get_po_extend(
            type="android.widget.EditText",
            name="新增乘机人姓名框文案",
            text="与乘机证件一致",
            global_num=0,
            local_num=1,
            touchable=True,
        )[0]
        passenger_username.click()
        passenger_username.set_text(passenger)

    @SleepWait(wait_time=1)
    def touch_passenger_card_type(self) -> None:
        """
        点击【证件类型】
        """
        passenger_card_type = self.device.get_po(
            type="android.widget.TextView", name="新增乘机人证件类型文案")
        passenger_card_type.click()
        logger.info("点击【证件类型】")

    @SleepWait(wait_time=1)
    def select_passenger_card_type(self, card_type: str) -> None:
        """
        选择合适的证件类型
        """
        passenger_card_type = self.device.get_po(
            type="android.widget.TextView", text=card_type)
        passenger_card_type.click()
        logger.info("选择【{}】".format(card_type))

    @SleepWait(wait_time=1)
    def enter_passenger_card_id(self, card_id: str) -> None:
        """
        录入乘客证件号码
        """
        passenger_card_id = self.device.get_po_extend(
            type="android.widget.EditText",
            name="新增乘机人证件号码文案",
            text="请输入证件号",
            global_num=0,
            local_num=1,
            touchable=True,
        )[0]
        passenger_card_id.click()
        passenger_card_id.set_text(card_id)

    @SleepWait(wait_time=1)
    def enter_passenger_phone_number(self, phone: str) -> None:
        """
        录入乘客手机号码
        """
        passenger_phone_number = self.device.get_po_extend(
            type="android.widget.EditText",
            name="新增乘机人手机框文案",
            global_num=0,
            local_num=1,
            touchable=True,
        )[0]
        passenger_phone_number.click()
        passenger_phone_number.set_text(phone)

    @SleepWait(wait_time=1)
    def submit_passenger_info(self) -> None:
        """
        点击【完成】按钮，提交乘客信息
        """
        file_name = join_path([get_images_dir(), "键盘隐藏.png"])
        self.device.hide_keyword(file_name=file_name)
        passenger_info = self.device.get_po_extend(
            type="android.widget.TextView",
            name="新增乘机人完成按钮",
            text="完成",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        passenger_info.click()

    @SleepWait(wait_time=3)
    def submit_passenger_info_confirm(self) -> None:
        """
        点击【确认无误】按钮，提交乘客信息
        """
        """
        passenger_info_confirm = self.device.get_po_extend(
            type="android.view.ViewGroup",
            name="android.view.ViewGroup",
            global_num=0,
            local_num=5,
            touchable=True,
        )[0]
        passenger_info_confirm.click()
        """
        file_name = join_path([get_images_dir(), "乘机人信息_确认无误.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (723, 1413)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(v=temp)

    @LoopFindElement(loop=5)
    # @SleepWait(wait_time=1)
    def add_passenger(self, passenger: str) -> None:
        """
        点击【确定】按钮，添加乘客
        """
        passenger_po = self.device.get_po_extend(
            type="android.widget.TextView",
            name="乘机人列表确定按钮",
            text="确定",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        passenger_po.click()
        logger.info("预定特价机票，已添加乘客: <{}>".format(passenger))

    @SleepWait(wait_time=1)
    def select_insecure(self) -> None:
        """
        选择【无保障】航意航延组合险
        """
        # 先滑屏
        self.device.quick_slide_screen(duration=0.5)
        insecure = self.device.get_po_extend(
            type="android.widget.TextView",
            name="航意航延组合险无保障标题",
            text="无保障",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        insecure.click()

    @SleepWait(wait_time=5)
    def touch_fill_order_next_step(self) -> None:
        """
        填订单界面，点击【下一步】
        """
        next_step = self.device.get_po_extend(
            type="android.widget.TextView",
            name="下一步",
            text="下一步",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        next_step.click()

    @SleepWait(wait_time=1)
    def is_duplicate_order(self) -> str:
        """
        如果用户已经下单，系统会有弹框提示，下单重复了
        """
        duplicate_order_1 = self.device.get_po(
            type="android.widget.TextView", text="我知道了")
        duplicate_order_2 = self.device.get_po(type="android.widget.TextView", name="android.widget.TextView",
                                               text="继续预订当前航班")
        duplicate_order_3 = self.device.get_po(
            type="android.widget.TextView", name="重复订单标题", text="行程冲突提示")
        if duplicate_order_1.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="重复订单提示文案",
                global_num=0,
                local_num=2,
                touchable=False,
            )[0]
            conflict_prompt_str = get_ui_object_proxy_attr(
                ui_object_proxy=conflict_prompt).get("text")
            duplicate_order_1.click()
            return conflict_prompt_str
        elif duplicate_order_2.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            conflict_prompt_str = get_ui_object_proxy_attr(
                ui_object_proxy=conflict_prompt).get("text")
            duplicate_order_2.click()
            return conflict_prompt_str
        elif duplicate_order_3.exists():
            conflict_prompt = self.device.get_po_extend(
                type="android.widget.TextView",
                name="重复订单提示文案",
                global_num=0,
                local_num=3,
                touchable=False,
            )[0]
            conflict_prompt_str = get_ui_object_proxy_attr(
                ui_object_proxy=conflict_prompt).get("text")
            self.device.touch((400, 500))  # 点击一个随机坐标，尽量靠近上半屏，相当于点击空白处，隐藏掉提示框
            return conflict_prompt_str
        else:
            return ""

    @SleepWait(wait_time=1)
    def touch_select_service_no_need(self) -> None:
        """
        选服务界面，点击【不用了，谢谢】
        """
        try:
            no_need = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="不用了，谢谢",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            no_need.click()
        except (PocoNoSuchNodeException, Exception):
            pass

    @SleepWait(wait_time=1)
    def touch_to_payment(self) -> None:
        """
        选服务界面，点击【去支付】
        """
        try:
            to_payment = self.device.get_po_extend(
                type="android.widget.TextView",
                name="去支付",
                text="去支付",
                global_num=0,
                local_num=2,
                touchable=False,
            )[0]
            to_payment.click()
        except (PocoNoSuchNodeException, Exception):
            pass

    @SleepWait(wait_time=3)
    def touch_insure_no(self) -> None:
        """
        选航空意外险界面，点击【否】
        """
        try:
            no = self.device.get_po_extend(
                type="android.widget.TextView",
                name="android.widget.TextView",
                text="否",
                global_num=0,
                local_num=1,
                touchable=False,
            )[0]
            no.click()
        except (PocoNoSuchNodeException, Exception):
            pass

    @SleepWait(wait_time=5)
    def touch_read_agree(self) -> None:
        """
        我已阅读并同意，点击【同意并支付】
        """
        try:
            agree = self.device.get_po_extend(
                type="android.widget.TextView",
                name="去支付",
                text="同意并支付",
                global_num=0,
                local_num=2,
                touchable=False,
            )[0]
            agree.click()
        except (PocoNoSuchNodeException, Exception):
            pass

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
        method = self.device.get_po(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text=payment_method
        )
        method.click()
        logger.info("点击选择【{}】".format(payment_method))

    def select_more_payment(self) -> bool:
        """
        当【同意并支付】后，特殊情况下，会出现支付小弹框，这个时候需要先判断是否存在小框，如果存在，则切换到通用支付选择界面
        """
        flag = False
        # 这个地方容易卡卡住，采用透底的方案执行该逻辑
        for _ in range(20):
            # 1. 检测是否到了安全收银台，安全收银台的定位特征是：【安全收银台】|【银行卡支付】
            try:
                safe_cash = self.device.get_po(
                    type="android.widget.TextView", name="android.widget.TextView", text="安全收银台"
                )
                if safe_cash.exists() is True:
                    flag = True
                    time.sleep(3)
                    break
            except (Exception,):
                pass
            try:
                bank_card_payment = self.device.get_po(
                    type="android.widget.TextView", name="android.widget.TextView", text="银行卡支付"
                )
                if bank_card_payment.exists() is True:
                    flag = True
                    time.sleep(3)
                    break
            except (Exception,):
                pass
            # 2. 检测到小弹框， 定位特征是：【更多付款方式】
            try:
                more_payment_type = self.device.get_po(
                    type="android.view.ViewGroup ", name="更多付款方式", desc="更多付款方式"
                )
                if more_payment_type.exists() is True:
                    logger.warning("元素定位方式检测到有小弹框，需要点击【更多付款方式】")
                    more_payment_type.click()
                    time.sleep(1)
                    try:
                        more_payment_type_inner = self.device.get_po(
                            type="android.view.ViewGroup ", name="更多付款方式", desc="更多付款方式"
                        )
                        if more_payment_type_inner.exists() is False:
                            flag = True
                            time.sleep(3)
                            break
                    except (Exception,):
                        pass
            except (Exception,):
                pass
            # 3. 检测到小弹框， 图像识别定位特征是：【更多付款方式】
            try:
                file_name = join_path([get_images_dir(), "更多付款方式.png"])
                if is_exists(file_name):
                    temp = self.device.get_cv_template(file_name=file_name)
                    if temp:
                        logger.warning("图像识别方式检测到有小弹框，需要点击【更多付款方式】")
                        self.device.touch(v=temp)
                        time.sleep(1)
                        temp_inner = self.device.get_cv_template(file_name=file_name)
                        if not temp_inner:
                            flag = True
                            time.sleep(3)
                            break
            except (Exception,):
                pass
            time.sleep(1)
        return flag

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

    @SleepWait(wait_time=1)
    def touch_wallet_payment(self) -> None:
        wallet = self.__get_wallet_element()
        wallet.click()

    @SleepWait(wait_time=1)
    def select_gift_card(self, payment_method: str) -> None:
        """选择对应的礼品卡"""
        gift_card = self.device.get_po(
            type="android.widget.TextView", name="android.widget.TextView", text=payment_method
        )
        gift_card.click()

    @SleepWait(wait_time=1)
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

    @SleepWait(wait_time=1)
    def touch_wallet_immediate_payment(self) -> None:
        """选择对应的礼品卡，点击【使用钱包全额抵扣，立即支付】"""
        wallet_immediate_payment = self.device.get_po(
            type="android.widget.TextView", name="android.widget.TextView", text="使用钱包全额抵扣，立即支付"
        )
        wallet_immediate_payment.click()

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

    @SleepWait(wait_time=1)
    def touch_bank_card_payment(self) -> None:
        """
        支付界面，选择【银行卡支付】
        """
        point_deduction = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="银行卡支付",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        point_deduction.click()

    def get_ticket_actual_amount(self) -> Decimal:
        """
        确定使用积分抵扣后，票据的实际支付金额
        """
        ticket_actual_amount = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            textMatches_inner=r"^¥\d+.\d*",
            global_num=0,
            local_num=2,
            touchable=False,
        )[0]
        actual_amount = ticket_actual_amount.get_text()
        actual_amount = Decimal(actual_amount[1:]) if isinstance(
            actual_amount, str) else 9999999999.9999999999
        return actual_amount

    def get_ticket_deduction_amount(self) -> Decimal:
        """
        使用积分抵扣的金额
        """
        tickect_deduction_amount = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            textMatches_inner=r"^-¥\d+.\d*",
            global_num=0,
            local_num=4,
            touchable=False,
        )[0]
        deduction_amount = tickect_deduction_amount.get_text()
        deduction_amount = Decimal(deduction_amount[2:]) if isinstance(deduction_amount,
                                                                       str) else -9999999999.9999999999
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
        payment_pass = payment_pass if isinstance(payment_pass, str) else str(payment_pass)
        for char in payment_pass:
            char_position = ctrip_soft_keyboard_position.get(char)
            self.device.touch(v=char_position)

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

    @SleepWait(wait_time=1)
    def get_order_with_payment_amount(self) -> Decimal:
        """获取支付成功后的订单金额"""
        payment_amount = -9999999999.9999999999
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
            payment_amount = Decimal(payment_amount) if isinstance(payment_amount, str) else payment_amount
        except Exception as e:
            logger.error(str(e))
        return payment_amount

    @LoopFindElementSubmit(loop=3, action="支付完成")
    def touch_payment_complete(self):
        """在支付成功界面，点击【完成】"""
        payment_complete_button = self.device.poco(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="完成"
        )
        payment_complete_button.click()
        logger.warning("点击支付成功界面的【完成】按钮.")

    @SleepWait(wait_time=1)
    def close_coupon_dialog(self) -> None:
        """支付完成后，会有一个优惠卷弹框，需要关闭"""
        try:
            coupon_dialog = self.device.get_po(
                type="android.view.ViewGroup", name="领券弹窗关闭按钮")
            if coupon_dialog.exists():
                coupon_dialog.click()
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有出现领券弹窗关闭按钮.")

    @SleepWait(wait_time=1)
    def expand_order_detail(self) -> None:
        """展开【详情/首页】"""
        try:
            file_name = join_path([get_images_dir(), "完成后的订单详情.png"])
            if is_exists(file_name):
                temp = self.device.get_cv_template(file_name=file_name)
            else:
                temp = (902, 202)  # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
            self.device.touch(v=temp)
            logger.info("展开【详情/首页】，接下来可以点击【查订单/开发票】")
        except Exception as e:
            logger.error("展开【详情/首页】元素失败，原因：{}".format(str(e)))

    @SleepWait(wait_time=5)
    def touch_order_detail(self) -> None:
        """点击【查订单/开发票】，进入订单详情界面"""
        try:
            order_detail = self.device.get_po(type="android.widget.TextView", name="android.widget.TextView",
                                              text="查订单/开发票")
            order_detail.click()
            logger.info("点击【查订单/开发票】，进入订单详情界面")
        except Exception as e:
            logger.error("点击点击【查订单/开发票】失败，原因：{}".format(str(e)))

    @SleepWait(wait_time=2)
    def close_important_trip_guidelines(self) -> None:
        """关闭出行前必读"""
        try:
            read_me = self.device.get_po(type="android.widget.TextView", name="浮层标题", text="出行前必读")
            if read_me.exists() is True:
                # 说明出现了出行前必读，需要关闭该窗口
                file_name = join_path([get_images_dir(), "关闭.png"])
                if is_exists(file_name):
                    temp = self.device.get_cv_template(file_name=file_name)
                else:
                    temp = (76, 367)  # Huawei Mate 20手机上对应的坐标位置，其他型号手机可能不是这个值
                self.device.touch(v=temp)
                logger.info("【出行前必读】小窗口，已关闭.")
            else:
                logger.info("【出行前必读】小窗口，不可点击")
        except (PocoNoSuchNodeException, Exception):
            logger.warning("没有检测到【出现前必读】小窗口弹出，可以直接进行下面的操作.")

    @SleepWait(wait_time=1)
    def touch_order_with_finish_button(self) -> None:
        """点击支付成功界面的【完成】按钮"""
        finish_button = self.device.get_po_extend(
            type="android.widget.TextView",
            name="android.widget.TextView",
            text="完成",
            global_num=0,
            local_num=1,
            touchable=False,
        )[0]
        logger.info("点击【完成】按钮, 关闭流程.")
        finish_button.click()

    @SleepWait(wait_time=1)
    def get_flight_ticket_with_order_id(self) -> str:
        """获取机票订单的id"""
        order_id = None
        try:
            poco = self.device.get_po(type="android.widget.TextView", name="pricePolicy_Text_订单号")
            order_id = poco.get_text().split("：")[-1].strip()
        except Exception as e:
            logger.error("获取携程订单id失败，原因：{}".format(str(e)))
        return order_id

    @SleepWait(wait_time=1)
    def get_flight_ticket_with_itinerary_id(self) -> str:
        """获取机票中乘客的行程单号，可能在出票中，那么就先结束流程，等待人工回填行程单号"""
        # 滑动屏幕三次
        for i in range(3):
            self.device.quick_slide_screen()
        itinerary_id = None
        try:
            poco = (
                self.device.poco("android.widget.FrameLayout")
                .offspring("android:id/content")
                .child("ctrip.android.view:id/a")
                .child("ctrip.android.view:id/a")
                .offspring("android.widget.LinearLayout")
                .offspring("android.widget.FrameLayout")
                .child("android.view.ViewGroup")
                .child("android.view.ViewGroup")
                .child("android.view.ViewGroup")
                .child("android.view.ViewGroup")
                .child("android.view.ViewGroup")[1]
                .offspring("PullRefreshScrollView_ScrollView")
                .child("android.view.ViewGroup")
                .child("android.view.ViewGroup")
                .offspring("@contactInfo")
                .offspring("contactInfo_Text_票号")[0]
            )
            if poco.exists() is True:
                itinerary_id = poco.get_text().split("：")[-1].strip()
        except (PocoNoSuchNodeException, Exception):
            logger.warning("出票中，没有查找到行程单.")
        return itinerary_id

    """
    # 为了调式方便，暂时注释
    def __del__(self) -> None:
        self.stop()
    """

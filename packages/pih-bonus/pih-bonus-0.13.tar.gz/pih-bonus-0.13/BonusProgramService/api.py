import ipih

from pih import A, strdict
from pih.tools import nnt
from pih.collections import PolibasePerson, BonusInformation

from datetime import datetime
import requests
import json


class BonusApi:

    @staticmethod
    def _make_call(data: strdict) -> strdict:
        url: str = (
            "https://cabinet.statix-pro.ru/webhooks/custom/pacific_ih.php?login=customer336&password=pacific20!"
        )
        response = requests.get(
            url=url, data=json.dumps(data), headers={"Content-type": "application/json"}
        )
        return response.json()

    @staticmethod
    def _create_bonus_card_data(value: PolibasePerson) -> strdict:
        bonus_information: BonusInformation = nnt(A.R_P.bonus_information(value).data)
        full_name_list: list[str] = value.FullName.split(A.D.SPLIT_SYMBOL)
        return {
            "operation_type": "create_client",
            "phone": value.telephoneNumber,
            "PIN": str(value.pin),
            # "gender": "male",
            "discount_percent": A.S.get(A.CT_S.BONUS_PROGRAM_DISCOUNT_PERCENT),
            "cashback_percent": A.S.get(A.CT_S.BONUS_PROGRAM_CASHBACK_PERCENT),
            "bonus_points": bonus_information.bonus_active,
            "total_paid_sum": bonus_information.money_all,
            "birth_date": A.D_F.datetime(value.Birth, A.CT.DATE_FORMAT),
            "first_name": full_name_list[1],
            "last_name": full_name_list[0],
            #"patronymic": full_name_list[2],
        }

    def create_bonus_card(self, value: PolibasePerson) -> str | None:
        data: strdict = BonusApi._make_call(BonusApi._create_bonus_card_data(value))
        return A.D.if_is_in(data["data"], "card_download_link", None)

    @staticmethod
    def _search_bonus_card_data(value: PolibasePerson) -> strdict:
        return {
            "operation_type": "search_client",
            "PIN": str(value.pin),
        }

    def get_data(self, value: PolibasePerson) -> strdict:
        return BonusApi._make_call(BonusApi._search_bonus_card_data(value))

    def exists_bonus_card(
        self, value: PolibasePerson, check_device_status: bool = False
    ) -> bool:
        data: strdict = self.get_data(value)
        result: bool = data["message"] != "Error: error 46 - pkpass file not found"
        if result and check_device_status:
            return data["data"]["device_status"] == 1
        return result

    def update_bonuses(self, value: PolibasePerson, data: int | None = None) -> bool:
        bonus_information: BonusInformation = A.R_P.bonus_information(value).data
        return BonusApi._check_on_success(
            BonusApi._make_call(
                BonusApi._update_card_data(value,
                    {"bonus_points": data or bonus_information.bonus_active}
                )
            )
        )

    def update_visit_datetime(self, value: PolibasePerson, data: datetime) -> bool:
        return BonusApi._check_on_success(
            BonusApi._make_call(
                BonusApi._update_card_data(
                    value,
                    {
                        "closest_visit_date": A.D_F.datetime(
                            data, A.CT.DATETIME_SECONDLESS_FORMAT
                        )
                    },
                )
            )
        )

    @staticmethod
    def _update_card_data(value: PolibasePerson, data: strdict) -> strdict:
        full_name_list: list[str] = value.FullName.split(A.D.SPLIT_SYMBOL)
        data["operation_type"] = "update_client"
        data["PIN"] = str(value.pin)
        data["first_name"] = full_name_list[1]
        data["last_name"] = full_name_list[0]
        return data

    def update_card(self, value: PolibasePerson, data: strdict) -> bool:
        return BonusApi._check_on_success(
            BonusApi._make_call(BonusApi._update_card_data(value, data))
        )

    @staticmethod
    def _remove_bonus_card_data(value: PolibasePerson) -> strdict:
        return {
            "operation_type": "delete_client",
            "PIN": str(value.pin),
        }

    @staticmethod
    def _check_on_success(value: strdict) -> bool:
        return value["message"] == "ok" and value["status"] == "ok"

    def remove_bonus_card(self, value: PolibasePerson) -> bool:
        if self.exists_bonus_card(value):
            A.A_E.remove(
                A.CT_E.POLIBASE_PERSON_BONUS_CARD_WAS_CREATED,
                (value.pin,),
            )
            return BonusApi._check_on_success(
                BonusApi._make_call(BonusApi._remove_bonus_card_data(value))
            )
        return False

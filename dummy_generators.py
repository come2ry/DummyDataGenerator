import json
import random
import pandas as pd  # type: ignore
from typing import List, Dict, Tuple, Callable, Any, Union, Optional, TypeVar, cast, overload
from mypy_extensions import TypedDict
from faker import Factory  # type: ignore
from datetime import date
from pykakasi import kakasi  # type: ignore
from dummy_types import (
    CreatorType,
    RowDictType
)
from dummy_masters import Master as M

f = Factory.create('ja_JP')
kakasi = kakasi()
kakasi.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
conv = kakasi.getConverter()
MAX_ITR_N = 10**10


class DummyTemplate(object):
    def __init__(self, n: Optional[int] = None) -> None:
        self.itr_index: int = 0
        self.n: int = MAX_ITR_N if n is None else n
        self.creator: Optional[CreatorType] = None
        self.router: Dict[str, CreatorType] = {}

        self.master_sexs: Dict[str, str] = M.get("SEX")
        self.master_department_categories: Dict[str, str] = M.get("DEPARTMENT_CATEGORIES")
        self.master_job_types: Dict[str, str] = M.get("JOB_TYPES")
        self.master_business_domains: Dict[str, str] = M.get("BUSINESS_DOMAINS")
        self.master_school_type: Dict[str, str] = M.get("SCHOOL_TYPE")
        self.master_school_grades: Dict[str, Dict[str, str]] = M.get("SCHOOL_GRADES")
        self.master_faculties: List[str] = M.get("FACULTIES")
        self.master_departments: List[str] = M.get("DEPARTMENTS")
        self.master_address_types: Dict[str, str] = M.get("ADDRESS_TYPES")
        self.master_company_statuses: Dict[str, str] = M.get("COMPANY_STATUSES")
        self.master_area_types: Dict[str, str] = M.get("AREA_TYPES")
        self.master_traffic_allowances: List[str] = M.get("TRAFFIC_ALLOWANCES")
        self.master_apply_statuses: Dict[str, str] = M.get("APPLY_STATUSES")
        self.master_tags: List[str] = f.words(30)

        self.dummy_profile_image_url: str = M.get("PROFILE_IMAGE_URL")
        self.dummy_company_url: str = M.get("COMPANY_URL")

        # 動的Matser
        # self.master_tags: List[str] = f.words(30)

        self.will__set_init: bool = True

    def __iter__(self):
        return self

    def __next__(self) -> RowDictType:
        if self.itr_index == self.n:
            raise StopIteration()

        self.itr_index += 1
        if self.will__set_init:
            self._set_init()
        dummy_row: RowDictType = dict([(key, creator()) for key, creator in self.router.items()])
        return dummy_row

    def _set_init(self) -> None:
        pass

    def get_header(self) -> List[str]:
        return list(self.router.keys())


class DummyUser(DummyTemplate):

    def __init__(self, n: Optional[int] = None) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            '@': self._at,
            'id': self._id,
            'department_category_id': self._department_category_id,
            'school_grade_id': self._school_grade_id,
            'email': self._mail,
            'phone': self._phone,
            'high_school': self._hight_school,
            'school': self._school,
            'faculty': self._faculty,
            'department': self._department,
            'profile_image_url': self._profile_image_url,
            'name_1': self._name_1,
            'name_2': self._name_2,
            'furi_1': self._furi_1,
            'furi_2': self._furi_2,
            'birthday': self._birthday,
            'password': self._password,
            'pr': self._pr,
            'future': self._future,
        }

        self.itr_name: str = ""
        self.itr_name2: str = ""
        self.itr_school_type_id: int = -1


    def _set_init(self) -> None:
        name = f.name()
        self.itr_name = cast(str, name)
        self.itr_name2 = conv.do(self.itr_name)
        self.itr_school_type_id = int(random.choices(
            list(self.master_school_type.keys()),
            weights=list({
                "大学": 70,
                "高等専門学校": 9,
                "短期大学": 2,
                "美術大学": 1,
                "大学大学院": 15,
                "専門学校": 4
            }.values()),
            k=1
        )[0])

    def _at(self) -> Dict[str, Callable[..., List[Dict[str, int]]]]:
        return {
            'user_business_domain_ids': self._at_business_domain_ids(),
            'user_job_type_id': self._at_job_type_ids(),
        }

    def _at_business_domain_ids(self) -> List[Dict[str, int]]:
        k = random.randint(1, 3)
        domain_ids = random.sample(list(self.master_business_domains.keys()), k=k)
        return [{'user_id': self._id(), 'domain_id': int(b)} for b in domain_ids]

    def _at_job_type_ids(self) -> List[Dict[str, int]]:
        k = random.randint(1, 3)
        job_type_ids = random.sample(list(self.master_job_types.values()), k=k)
        return [{'user_id': self._id(), 'job_type_id_id': int(b)} for b in job_type_ids]

    def _id(self) -> int:
        return self.itr_index

    def _name_1(self) -> str:
        return self.itr_name.split(' ')[0]

    def _name_2(self) -> str:
        return self.itr_name.split(' ')[1]

    def _furi_1(self) -> str:
        return self.itr_name2.split(' ')[0]

    def _furi_2(self) -> str:
        return self.itr_name2.split(' ')[1]

    def _mail(self) -> str:
        return f.email()

    def _phone(self) -> str:
        return "060" + ''.join(map(str, random.choices(range(10), k=8)))

    def _hight_school(self) -> str:
        return f.town()+"高校"

    def _school(self) -> str:
        # return random.choice(self.master_schools)
        return f.town()+self.master_school_type[str(self.itr_school_type_id)]

    def _faculty(self) -> str:
        return random.choice(self.master_faculties)

    def _department(self) -> str:
        return random.choice(self.master_departments)

    def _department_category_id(self) -> int:
        return int(random.choice(list(self.master_department_categories.keys())))

    def _school_grade_id(self) -> int:
        return int(random.choice(list(self.master_school_grades[self.master_school_type[str(self.itr_school_type_id)]].keys())))

    def _birthday(self) -> date:
        # pattern="%Y-%m-%d %H:%M:%S"
        return f.date_between(start_date=date(year=1995, month=1, day=1), end_date=date(year=2002, month=1, day=1))

    def _sex_id(self) -> int:
        return int(random.choice(list(self.master_sexs.keys())))

    def _profile_image_url(self) -> str:
        return self.dummy_profile_image_url

    def _pr(self) -> str:
        return str(random.randint(0, 10000))

    def _future(self) -> str:
        return "\\n".join(f.text(random.randint(5, 400)).splitlines()) if random.randint(0, 10) != 0 else ""

    def _password(self) -> str:
        return "password"


class DummyAddress(DummyTemplate):

    def __init__(self, n: Optional[int] = None) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            '@': self._at,
            'id': self._id,
            'company_id': self._company_id,
            'address_type_id': self._address_type_id,
            'area_id': self._area_type,
            'title': self._address_title,
            'access': self._access,
            'zipcode': self._zipcode,
            'address_1': self._address_1,
            'address_2': self._address_2,
            'address_3': self._address_3,
            'address_4': self._address_4
        }
        self.company_num: int = 0
        self.itr_address_type_id: int = 0
        self.itr_address_list: List[Any] = []

    def _set_init(self) -> None:
        self.itr_address_list = [f.prefecture(), f.city(
        ), f.town(), f.chome()+f.ban(), f.building_name()+f.gou()]
        self.itr_address_type_id = int(random.choices(
            list(self.master_address_types.keys()),
            weights=list({
                "本社": 60,
                "支社": 25,
                "その他": 10,
            }.values()),
            k=1
        )[0])

        if self.itr_address_type_id == 0:
            self.company_num += 1

    def _at(self) -> Dict[str, Callable[..., Dict[str, str]]]:
        return {
            'area': self._at_area(),
        }

    def _at_area(self) -> Dict[str, str]:
        return {
            'area_type': "city",
            'area': ','.join(self.itr_address_list[:2]),
            'description': ""
        }

    def _id(self) -> int:
        return self.itr_index

    def _company_id(self) -> int:
        return self.company_num

    def _address_type_id(self) -> int:
        return self.itr_address_type_id

    def _area_type(self) -> str:
        return random.choice(list(self.master_area_types.keys()))

    def _address_title(self) -> str:
        address_title = "" if self.itr_address_type_id != 1 else self.itr_address_list[0]
        address_title += self.master_address_types[str(self.itr_address_type_id)]
        return address_title

    def _access(self) -> str:
        return f"{self.itr_address_list[2]}駅から徒歩{random.randint(1, 20)}分"

    def _zipcode(self) -> str:
        return f.zipcode()

    def _address_1(self) -> str:
        return self.itr_address_list[0]

    def _address_2(self) -> str:
        return self.itr_address_list[1]

    def _address_3(self) -> str:
        return "".join(self.itr_address_list[2:4])

    def _address_4(self) -> str:
        return self.itr_address_list[4]


class DummyCompany(DummyAddress):

    def __init__(self, n: Optional[int] = None) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            '@': self._at,
            'id': self._id,
            'acoount_status_id': self._company_account_status_id,
            'company_name': self._company,
            'profile_image_url': self._profile_image_url,
            'company_url': self._company_url,
            'employees': self._employees,
            'representative_name': self._representative_name,
            'capital': self._capital,
            'established_at': self._established
        }

    def _at(self) -> Dict[str, Callable[..., Dict[str, str]]]:
        return {
            'description': self._at_description(),
            'company_business_domains': self._at_company_business_domains(),
        }

    def _at_description(self) -> Dict[str, str]:
        return {
            'description': "\\n".join(f.text(random.randint(400, 1000)).splitlines()) if random.randint(0, 10) != 0 else "",
        }

    def _at_company_business_domain_ids(self) -> List[Dict[str, int]]:
        k = random.randint(1, 4)
        domain_ids = random.sample(list(self.master_business_domains.keys()), k=k)
        return [{'company_id': self._id(), 'domain_id': int(b)} for b in domain_ids]

    def _id(self) -> int:
        return self.itr_index

    def _company_account_status_id(self) -> int:
        return int(random.choices(
            list(self.master_company_statuses.keys()),
            weights=list({
                "スタンダード": 8,
                "プレミアム": 1,
                "退会済み": 2
            }.values()),
            k=1
        )[0])

    def _profile_image_url(self) -> str:
        return self.dummy_profile_image_url

    def _company_url(self) -> str:
        return self.dummy_company_url

    def _company(self) -> str:
        return f.last_name()+"株式会社"

    def _employees(self) -> str:
        n = random.randint(10, 3000)
        return str(n)[:2]+"0"*(len(str(n))-2)

    def _representative_name(self) -> str:
        return f.name()

    def _capital(self) -> str:
        n = random.randint(1000000, 100000000)
        return str(n)[:2]+"0"*(len(str(n))-2)

    def _established(self) -> int:
        return random.randint(1970, 2020)


class DummyJobPost(DummyAddress):

    def __init__(self, n: Optional[int] = None) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            '@': self._at,
            'id': self._id,
            'company_id': self._company_id,
            'address_id': self._address_id,
            'job_type_id': self._job_type_id,
            'acquirable_skills': self._acquirable_skills,
            'job_content': self._job_content,
            'job_image_url': self._job_image_url,
            'requirement_text': self._requirement_text,
            'title': self._title,
            'subtitle': self._subtitle,
            'traffic_allowance': self._traffic_allowance,
            'salary': self._salary,
            'work_days': self._work_days,
            'work_hours': self._work_hours,
            'is_closed': self._is_closed,
        }

        self.itr_houry_wage: Optional[int] = None
        self.itr_work_hours: Optional[int] = None
        self.itr_work_days: Optional[int] = None
        self.itr_address_id: Optional[int] = None
        self.itr_address: RowDictType = {}
        self.itr_salary: Union[Tuple[str, str, int],
                                Tuple[str, str, int, int], None] = None

        self.will__set_init: bool = False

    def set_init(self, address_row: Optional[RowDictType] = None) -> None:
        super()._set_init()
        self.itr_houry_wage = (random.randint(1000, 3249)//250)*250
        self.itr_work_hours = random.randint(3, 10)
        self.itr_work_days = random.randint(1, 5)
        self.itr_monthly_salary = self.itr_houry_wage * \
            self.itr_work_hours*self.itr_work_days
        self.itr_address_id = 1

        r: int = random.randint(1, 4)
        if r == 1:
            self.itr_salary = ("時給", random.choice(
                ["<", "=", ">"]), self.itr_houry_wage)
        elif r == 2:
            self.itr_salary = ("時給", "〜", self.itr_houry_wage, self.itr_houry_wage +
                                random.choice([500, 1000, 1500, 2000, 2500, 3000]))
        elif r == 3:
            self.itr_salary = ("月給", random.choice(
                ["<", "=", ">"]), self.itr_monthly_salary)
        else:
            self.itr_salary = ("月給", "〜", self.itr_monthly_salary, self.itr_monthly_salary +
                                random.choice([5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000]))

        if address_row is None:
            raise TypeError(
                "set_init() missing required argument 'addres_row' (pos 1)")
            exit(0)

        self.set_address(cast(RowDictType, address_row))

    def set_address(self, address_row: RowDictType) -> None:
        self.itr_address = address_row

    def _at(self) -> Dict[str, Callable[..., Dict[str, str]]]:
        return {
            'pv': self._at_pv(),
            'tags': self._at_tags(),
            'post_content': self._at_post_content()
        }

    def _at_pv(self) -> Dict[str, int]:
        return {
            'post_id': self._id(),
            'count': random.randint(0, 1000)
        }

    def _at_tags(self) -> List[Dict[str, int]]:
        k = random.randint(1, 4)
        tag_ids = random.sample(list(self.master_tags.keys()), k=k)
        return [{'post_id': self._id(), 'tag_id': int(t)} for t in tag_ids]

    def _at_post_content(self) -> Dict[str, str]:
        contents: Dict[str, Union[str, List[str], List[Dict[str, str]]]] = {}
        contents["gaiyo"] = f.text(random.randint(100, 1000))
        contents["gyomu"] = "・"+"\\n・".join(f.text(random.randint(200, 400)).splitlines())
        contents["steps"] = [f.text(random.randint(40, 100))
                            for _ in range(random.randint(3, 5))]
        contents["shains"] = [{"shain": self.dummy_profile_image_url, "message": f.text(
            100)} for _ in range(random.randint(1, 3))]

        return {
            'post_content': json.dumps(contents, ensure_ascii=False)
        }

    def _id(self) -> int:
        return self.itr_index

    def _job_type_id(self) -> int:
        return int(random.choice(list(self.master_job_types.keys())))

    def _job_content(self) -> str:
        # return ",".join(f.words(random.randint(1, 3)))
        return f.word()

    def _company_id(self) -> int:
        return cast(int, self.itr_address.get("company_id", -1))

    def _address_id(self) -> int:
        return cast(int, self.itr_address.get("id", -1))

    def _job_image_url(self) -> str:
        return self.dummy_profile_image_url

    def _acquirable_skills(self) -> str:
        return "\\n".join(f.text(random.randint(200, 400)).splitlines())

    def _requirement_text(self) -> str:
        return "・"+"\\n・".join(f.text(random.randint(200, 400)).splitlines())

    def _title(self) -> str:
        return "\\n".join(f.text(random.randint(50, 100)).splitlines())

    def _subtitle(self) -> str:
        return "\\n".join(f.text(random.randint(50, 100)).splitlines())

    def _traffic_allowance(self) -> str:
        return random.choice(self.master_traffic_allowances)

    def _salary(self) -> str:
        if self.itr_salary is None:
            raise(TypeError)
            exit(0)
        return ",".join(map(str, self.itr_salary))

    def _work_days(self) -> int:
        if self.itr_work_days is None:
            raise(TypeError)
            exit(0)
        return self.itr_work_days

    def _work_hours(self) -> int:
        if self.itr_work_hours is None:
            raise(TypeError)
            exit(0)
        return self.itr_work_hours

    def _is_closed(self) -> int:
        return random.choices([0, 1], weights=[95, 5], k=1)[0]



class DummyJobApply(DummyTemplate):

    def __init__(self, n: Optional[int] = None) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            '@': self._at,
            'id': self._id,
            '参加ステータスID': self._apply_status_id,
            '投稿ID': self._post_id,
            'ユーザーID': self._user_id,
            '勤務日数': self._work_days,
            '勤務時間数': self._work_hours,
            '志望動機': self._motivation,
            '備考': self._remark
        }

        self.itr_user_id: Optional[int] = None
        self.itr_post_id: Optional[int] = None

        self.will__set_init: bool = False

    def set_init(self, user_id: Optional[int] = None, post_id: Optional[int] = None) -> None:
        super()._set_init()

        if user_id is None or post_id is None:
            errors = []
            if user_id is None:
                errors += ["'user_id'"]
            if post_id is None:
                errors += ["'post_id'"]
            error_message = ", ".join(errors)

            raise TypeError(
                f"set_init() missing required argument {error_message}")
            exit(0)

        self.itr_user_id = user_id
        self.itr_post_id = post_id

    def _id(self) -> int:
        return self.itr_index

    def _apply_status_id(self) -> int:
        return int(random.choice(list(self.master_apply_statuses.keys())))

    def _post_id(self) -> int:
        return cast(int, self.itr_post_id)

    def _user_id(self) -> int:
        return cast(int, self.itr_user_id)

    def _work_days(self) -> int:
        return random.randint(3, 10)

    def _work_hours(self) -> int:
        return random.randint(1, 5)

    def _motivation(self) -> str:
        return "\\n".join(f.text(random.randint(100, 400)).splitlines())

    def _remark(self) -> str:
        return "\\n".join(f.text(random.randint(100, 400)).splitlines())


class DummyJobFav(DummyTemplate):

    def __init__(self, n: Optional[int] = None) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            '投稿ID': self._post_id,
            'ユーザーID': self._user_id
        }

        self.itr_user_id: Optional[int] = None
        self.itr_post_id: Optional[int] = None

        self.will__set_init: bool = False

    def set_init(self, user_id: Optional[int] = None, post_id: Optional[int] = None) -> None:
        super()._set_init()

        if user_id is None or post_id is None:
            errors = []
            if user_id is None:
                errors += ["'user_id'"]
            if post_id is None:
                errors += ["'post_id'"]
            error_message = ", ".join(errors)

            raise TypeError(
                f"set_init() missing required argument {error_message}")
            exit(0)

        self.itr_user_id = user_id
        self.itr_post_id = post_id

    def _id(self) -> int:
        return self.itr_index

    def _post_id(self) -> int:
        return cast(int, self.itr_post_id)

    def _user_id(self) -> int:
        return cast(int, self.itr_user_id)

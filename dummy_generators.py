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


class DummyTemplate(object):
    def __init__(self, n: int) -> None:
        self.itr_index: int = 0
        self.n: int = n
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

        self.dummy_profile_image_url: str = M.get("PROFILE_IMAGE_URL")
        self.dummy_company_url: str = M.get("COMPANY_URL")

        # 動的Matser
        self.master_tags: List[str] = f.words(30)

    def __iter__(self):
        return self

    def __next__(self) -> RowDictType:
        return {}

    def get_header(self) -> List[str]:
        return list(self.router.keys())


class DummyUser(DummyTemplate):

    def __init__(self, n: int) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            'ID': self._id,
            '姓': self._second_name,
            '名': self._first_name,
            'セイ': self._second_name2,
            'メイ': self._first_name2,
            'メールアドレス': self._mail,
            '電話番号': self._tel,
            '大学名': self._school,
            '学部': self._faculty,
            '学科': self._department,
            '学科系統ID': self._department_category_id,
            '学年ID': self._school_grade_id,
            '生年月日': self._birthday,
            '性別ID': self._sex_id,
            'プロフィール画像': self._profile_image_url,
            '希望業界IDs': self._business_domain_ids,
            '希望職種IDs': self._job_type_ids,
            '自己PR': self._pr,
            '将来': self._future,
            'パスワード': self._password
        }

        self.itr_name: str = ""
        self.itr_name2: str = ""
        self.itr_school_type_id: int = -1

    def __iter__(self) -> 'DummyUser':
        return self

    def __next__(self) -> RowDictType:
        if self.itr_index == self.n:
            raise StopIteration()

        self.itr_index += 1
        self.set_init(f.name())
        dummy_row: RowDictType = dict([(key, creator())
                                       for key, creator in self.router.items()])
        return dummy_row

    def set_init(self, name: Optional[str] = None) -> None:
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

    def _id(self) -> int:
        return self.itr_index

    def _second_name(self) -> str:
        return self.itr_name.split(' ')[0]

    def _first_name(self) -> str:
        return self.itr_name.split(' ')[1]

    def _second_name2(self) -> str:
        return self.itr_name2.split(' ')[0]

    def _first_name2(self) -> str:
        return self.itr_name2.split(' ')[1]

    def _mail(self) -> str:
        return f.email()

    def _tel(self) -> str:
        return "060" + ''.join(map(str, random.choices(range(10), k=8)))

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

    def _birthday(self) -> str:
        # pattern="%Y-%m-%d %H:%M:%S"
        return str(f.date_between(start_date=date(year=1995, month=1, day=1), end_date=date(year=2002, month=1, day=1)))

    def _sex_id(self) -> int:
        return int(random.choice(list(self.master_sexs.keys())))

    def _profile_image_url(self) -> str:
        return self.dummy_profile_image_url

    def _business_domain_ids(self) -> str:
        return ",".join(random.sample(list(self.master_business_domains.keys()), k=random.randint(1, 3)))

    def _job_type_ids(self) -> str:
        return ",".join(random.sample(list(self.master_job_types.values()), k=random.randint(1,3)))

    def _pr(self) -> str:
        return str(random.randint(0, 10000))

    def _future(self) -> str:
        return "\\n".join(f.text(random.randint(5, 400)).splitlines()) if random.randint(0, 10) != 0 else ""

    def _password(self) -> str:
        return "password"


class DummyAddress(DummyTemplate):

    def __init__(self, n: int) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            'ID': self._id,
            '会社ID': self._company_id,
            '住所タイプID': self._address_type_id,
            'エリアタイプ': self._area_type,
            'タイトル': self._address_title,
            'エリア': self._area,
            'エリア備考': self._area_description,
            'アクセス': self._access,
            '郵便番号': self._zipcode,
            '住所1': self._address_1,
            '住所2': self._address_2,
            '住所3': self._address_3,
            '住所4': self._address_4
        }
        self.company_num: int = 0
        self.itr_address_type_id: int = 0
        self.itr_address_list: List[Any] = []

    def __iter__(self) -> 'DummyAddress':
        return self

    def __next__(self) -> RowDictType:
        if self.itr_index == self.n:
            raise StopIteration()

        self.itr_index += 1
        self.set_init()
        dummy_row: RowDictType = dict([(key, creator())
                                       for key, creator in self.router.items()])
        return dummy_row

    def set_init(self) -> None:
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

    def _area(self) -> str:
        return ','.join(self.itr_address_list[:2])

    def _area_description(self) -> str:
        return ""

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

    def __init__(self, n: int) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            'ID': self._id,
            '会社名': self._company,
            '事業領域IDs': self._business_domain_ids,
            'アカウントステータスID': self._company_status_id,
            '説明': self._description,
            'プロフィール画像': self._profile_image_url,
            '会社URL': self._company_url,
            '従業員数': self._employees,
            '代表名': self._representative_name,
            '資本金': self._capital,
            '設立年': self._established
        }

    def __iter__(self) -> 'DummyCompany':
        return self

    def __next__(self) -> RowDictType:
        if self.itr_index == self.n:
            raise StopIteration()

        self.itr_index += 1
        self.set_init()
        dummy_row: RowDictType = dict([(key, creator())
                                       for key, creator in self.router.items()])
        return dummy_row

    def set_init(self) -> None:
        super().set_init()

    def _id(self) -> int:
        return self.itr_index

    def _business_domain_ids(self) -> str:
        return ",".join(random.sample(self.master_business_domains.keys(), k=random.randint(1, 4)))

    def _company_status_id(self) -> int:
        return int(random.choices(
            list(self.master_company_statuses.keys()),
            weights=list({
                "スタンダード": 8,
                "プレミアム": 1,
                "退会済み": 2
            }.values()),
            k=1
        )[0])


    def _description(self) -> str:
        return "\\n".join(f.text(random.randint(400, 1000)).splitlines()) if random.randint(0, 10) != 0 else ""

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

    def __init__(self, n: int) -> None:
        super().__init__(n)
        self.router: Dict[str, CreatorType] = {
            'ID': self._id,
            '会社ID': self._company_id,
            '住所ID': self._address_id,
            'PV': self._pv,
            '特徴': self._tags,
            '職種ID': self._job_type_id,
            '仕事内容': self._job_content,
            '身につくスキルs': self._acquireble_skills,
            '募集テキスト': self._post_content_text,
            '仕事イメージ画像': self._job_image_url,
            'タイトル': self._title,
            'サブタイトル': self._subtitle,
            '交通費支給': self._traffic_allowance,
            '給与': self._salary,
            '勤務日数': self._work_days,
            '勤務時間数': self._work_hours,
            '募集中': self._is_closed,
        }
        self.itr_houry_wage: Optional[int] = None
        self.itr_work_hours: Optional[int] = None
        self.itr_work_days: Optional[int] = None
        self.itr_address_id: Optional[int] = None
        self.itr_address: RowDictType = {}
        self.itr_salary: Union[Tuple[str, str, int],
                               Tuple[str, str, int, int], None] = None

    def __iter__(self) -> 'DummyJobPost':
        return self

    def __next__(self) -> RowDictType:
        if self.itr_index == self.n:
            raise StopIteration()

        self.itr_index += 1
        dummy_row: RowDictType = dict([(key, creator())
                                       for key, creator in self.router.items()])
        return dummy_row

    def set_init(self, address_row: Optional[RowDictType] = None) -> None:
        super().set_init()
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
            self.itr_salary = ("月給", "〜", self.itr_houry_wage, self.itr_monthly_salary +
                               random.choice([5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000]))

        if address_row is None:
            raise TypeError(
                "set_init() missing required argument 'addres_row' (pos 1)")
            exit(0)

        self.set_address(cast(RowDictType, address_row))

    def set_address(self, address_row: RowDictType) -> None:
        self.itr_address = address_row

    def _id(self) -> int:
        return self.itr_index

    def _tags(self) -> str:
        tags: List[str] = []
        n: int = random.randint(1, 10)
        for i in range(n):
            tag: str
            if random.randint(1, 10) <= 9:
                tag = random.choice(self.master_tags)
            else:
                for _ in range(10):
                    tag = f.word()
                    if tag in self.master_tags:
                        continue
                    self.master_tags.append(tag)
                    break
            tags.append(tag)
        return ",".join(tags)

    def _job_type_id(self) -> int:
        return int(random.choice(list(self.master_job_types.keys())))

    def _job_content(self) -> str:
        return f.words(random.randint(1, 3))

    def _acquireble_skills(self) -> str:
        return ",".join(f.words(random.randint(1, 10)))

    def _post_content_text(self) -> str:
        contents: Dict[str, Union[str, List[str], List[Dict[str, str]]]] = {}
        contents["gaiyo"] = f.text(random.randint(100, 1000))
        contents["steps"] = [f.text(random.randint(40, 100))
                             for _ in range(random.randint(3, 5))]
        contents["shains"] = [{"shain": self.dummy_profile_image_url, "message": f.text(
            100)} for _ in range(random.randint(1, 3))]
        return json.dumps(contents, ensure_ascii=False)

    def _company_id(self) -> int:
        return cast(int, self.itr_address.get("会社ID", -1))

    def _address_id(self) -> int:
        return cast(int, self.itr_address.get("ID", -1))

    def _job_image_url(self) -> str:
        return cast(str, self.dummy_profile_image_url)

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

    def _pv(self) -> int:
        return random.randint(0, 1000)

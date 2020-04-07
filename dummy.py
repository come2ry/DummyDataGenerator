import csv
import sys
import random
from collections import deque
from typing import List, Dict, Deque, Any, Optional, cast
from dummy_generators import (
    DummyUser,
    DummyCompany,
    DummyAddress,
    DummyJobPost,
    DummyJobApply,
    DummyJobFav
)
from dummy_types import (
    RowDictType
)

class Dummy(object):

    def __init__(self, n: int) -> None:
        self.n: int = n
        self.itr_index: int = 0
        self.dummy_user_creater: 'DummyUser' = DummyUser()
        self.dummy_company_creater: 'DummyCompany' = DummyCompany()
        self.dummy_address_creater: 'DummyAddress' = DummyAddress()
        self.dummy_job_post_creater: 'DummyJobPost' = DummyJobPost()
        self.dummy_job_apply_creater: 'DummyJobApply' = DummyJobApply()
        self.dummy_job_fav_creater: 'DummyJobFav' = DummyJobFav()
        self.address_queue: Deque[dict] = deque([])
        self.user_queue: Deque[int] = deque([])
        self.headers: Dict[str, List[str]] = {
            'user': list(self.dummy_user_creater.router.keys()),
            'address': list(self.dummy_address_creater.router.keys()),
            'company': list(self.dummy_company_creater.router.keys()),
            'job_post': list(self.dummy_job_post_creater.router.keys()),
            'job_apply': list(self.dummy_job_apply_creater.router.keys()),
            'job_fav': list(self.dummy_job_fav_creater.router.keys())
        }


    def __iter__(self) -> 'Dummy':
        return self

    def __next__(self) -> Dict[str, RowDictType]:
        if self.itr_index == self.n:
            raise StopIteration()

        self.itr_index += 1

        dummy_user_row: dict = next(self.dummy_user_creater)
        dummy_address_row: dict = next(self.dummy_address_creater)
        row: Dict[str, RowDictType] = {'user': dummy_user_row, 'address': dummy_address_row}

        if self.itr_index > 500:
            self.address_queue.popleft()
        self.address_queue.append(dummy_address_row)
        if self.itr_index > 500:
            self.user_queue.popleft()
        self.user_queue.append(cast(int, dummy_user_row.get('ID')))

        if self.itr_index == 1 or dummy_address_row.get('住所タイプID') == 1:
            dummy_company_row: RowDictType = next(self.dummy_company_creater)
            row['company'] = dummy_company_row

        if random.randint(1, 10) <= 7:
            self.dummy_job_post_creater.set_init(random.choice(self.address_queue))
            dummy_job_post_row: RowDictType = next(self.dummy_job_post_creater)
            row['job_post'] = dummy_job_post_row

            self.dummy_job_apply_creater.set_init(user_id=random.choice(self.user_queue), post_id=cast(int, dummy_job_post_row.get('ID')))
            dummy_job_apply_row: RowDictType = next(self.dummy_job_apply_creater)
            row['job_apply'] = dummy_job_apply_row

            self.dummy_job_fav_creater.set_init(user_id=random.choice(self.user_queue), post_id=cast(int, dummy_job_post_row.get('ID')))
            dummy_job_fav_row: RowDictType = next(self.dummy_job_fav_creater)
            row['job_fav'] = dummy_job_fav_row

        return row


    def get_header(self, key: str) -> List[str]:
        header: Optional[List[str]] = self.headers.get(key, None)
        if header is None:
            assert(f"{key}は存在しません")
            return []

        return header

    def get_indexs(self) -> Dict[str, int]:
        return {
            'user': self.dummy_user_creater._id(),
            'address': self.dummy_address_creater._id(),
            'company': self.dummy_company_creater._id(),
            'job_post': self.dummy_job_post_creater._id(),
            'job_apply': self.dummy_job_apply_creater._id(),
            'job_fav': self.dummy_job_fav_creater._id()
        }

if __name__ == '__main__':
    def main(n: int) -> None:
        with \
            open('example_csv/dummy_user.csv', 'w', encoding='utf-8') as u_fp, \
            open('example_csv/dummy_address.csv', 'w', encoding='utf-8') as a_fp, \
            open('example_csv/dummy_company.csv', 'w', encoding='utf-8') as c_fp, \
            open('example_csv/dummy_job_post.csv', 'w', encoding='utf-8') as jp_fp, \
            open('example_csv/dummy_job_apply.csv', 'w', encoding='utf-8') as ja_fp, \
            open('example_csv/dummy_job_fav.csv', 'w', encoding='utf-8') as jf_fp:

            u_writer = csv.writer(u_fp)
            a_writer = csv.writer(a_fp)
            c_writer = csv.writer(c_fp)
            jp_writer = csv.writer(jp_fp)
            ja_writer = csv.writer(ja_fp)
            jf_writer = csv.writer(jf_fp)

            dummy_creater: Dummy = Dummy(n)
            u_writer.writerow(dummy_creater.get_header('user'))
            a_writer.writerow(dummy_creater.get_header('address'))
            c_writer.writerow(dummy_creater.get_header('company'))
            jp_writer.writerow(dummy_creater.get_header('job_post'))
            ja_writer.writerow(dummy_creater.get_header('job_apply'))
            jf_writer.writerow(dummy_creater.get_header('job_fav'))

            for i, dummy_rows in enumerate(dummy_creater):
                # print(f"{i}: ", end="")

                for key, value in dummy_rows.items():
                    if key == 'user':
                        u_writer.writerow(list(value.values()))
                    elif key == 'address':
                        a_writer.writerow(list(value.values()))
                    elif key == 'company':
                        c_writer.writerow(list(value.values()))
                    elif key == 'job_post':
                        jp_writer.writerow(list(value.values()))
                    elif key == 'job_apply':
                        ja_writer.writerow(list(value.values()))
                    elif key == 'job_fav':
                        jf_writer.writerow(list(value.values()))

                sys.stdout.write("\rNow count is... %d" % i)
                sys.stdout.flush()

            results: Dict[str, int] = dummy_creater.get_indexs()
            print("\nCreated lines: ", end="")
            print(results)

    while 1:
        try:
            N: int = int(input('何行生成しますか？(int)'))
            break
        except ValueError:
            print("算用数字を入力してください(ex. 12)")
            continue
        except Exception as e:
            raise(e)

    main(N)

import requests
from pprint import pprint as pp
import time
import datetime
import pandas as pd
import os

C_END = "\033[0m"
C_BOLD = "\033[1m"
C_INVERSE = "\033[7m"
C_BLACK = "\033[30m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_PURPLE = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BGBLACK = "\033[40m"
C_BGRED = "\033[41m"
C_BGGREEN = "\033[42m"
C_BGYELLOW = "\033[43m"
C_BGBLUE = "\033[44m"
C_BGPURPLE = "\033[45m"
C_BGCYAN = "\033[46m"
C_BGWHITE = "\033[47m"

# 대분류 이름
pandarank_category_all_lists = ['카테고리 전체', '패션의류', '패션잡화', '화장품/미용', '디지털/가전', '가구/인테리어', '출산/육아', '식품', '스포츠/레저', '생활/건강', '여가/생활편의']
# 대분류
pandarank_category_all_num_lists = ['00000000', '50000000', '50000001', '50000002', '50000003', '50000004', '50000005', '50000006', '50000007', '50000008', '50000009']
# 대분류 + 중분류(2차분류)
pandarank_category_first_num_lists = ['50000000', '50000001', '50000002', '50000003', '50000004', '50000005', '50000006', '50000007', '50000008', '50000009',  # ⬅ 대분류
                                      '50000167', '50000169', '50000173', '50000174', '50000175', '50000176', '50000177', '50000178', '50000179', '50000180',  # ⬇ 중분류(2차분류)
                                      '50000181', '50000182', '50000166', '50000183', '50000184', '50000185', '50000186', '50000189', '50000190', '50000194',
                                      '50000195', '50000192', '50000193', '50000191', '50000202', '50000200', '50000197', '50000198', '50000199', '50000196',
                                      '50000201', '50000151', '50000091', '50000205', '50000089', '50000153', '50000208', '50000209', '50000210', '50000211',
                                      '50000206', '50000213', '50000214', '50000212', '50000204', '50000087', '50000088', '50000090', '50000152', '50000092',
                                      '50000093', '50000094', '50000095', '50000096', '50000097', '50000098', '50000099', '50000100', '50000101', '50000102',
                                      '50000103', '50000104', '50000105', '50000106', '50000107', '50000108', '50000109', '50000110', '50000111', '50000112',
                                      '50000113', '50000154', '50000114', '50000115', '50000116', '50000117', '50000118', '50000119', '50000120', '50000121',
                                      '50000122', '50000123', '50000124', '50000125', '50000126', '50000127', '50000128', '50000129', '50000130', '50000131',
                                      '50000132', '50000133', '50000134', '50000135', '50000136', '50000137', '50000138', '50007135', '50000139', '50000140',
                                      '50007127', '50000141', '50000142', '50000143', '50000144', '50000145', '50000159', '50000160', '50000146', '50000147',
                                      '50000148', '50000149', '50000150', '50000026', '50000023', '50000024', '50011940', '50012460', '50012520', '50012620',
                                      '50012782', '50013360', '50013520', '50013960', '50013881', '50014240', '50000027', '50000028', '50000029', '50000161',
                                      '50000162', '50000163', '50000164', '50000030', '50000031', '50000033', '50000034', '50000035', '50000036', '50000037',
                                      '50000038', '50000039', '50000040', '50000041', '50000042', '50000045', '50000046', '50000048', '50000049', '50000050',
                                      '50000051', '50000052', '50000053', '50000020', '50000021', '50000022', '50000165', '50000158', '50000054', '50000055',
                                      '50000056', '50000057', '50000156', '50000155', '50000058', '50000061', '50000062', '50000063', '50000064', '50000065',
                                      '50000066', '50000067', '50000068', '50000069', '50000070', '50000071', '50000072', '50000073', '50000074', '50000079',
                                      '50000080', '50000075', '50000157', '50000076', '50000077', '50000078', '50007252', '50007256', '50007261', '50007286',
                                      ]


keyword_csv_file_path = "pandarank_keywords.csv"


def get_keyword_pandarank():
    
    pandarank_keyword_lists = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    
    count = 1
    for i in pandarank_category_first_num_lists:

        response = requests.get(f'https://pandarank.net/api/categories/home/{i}', headers=headers).json()

        for j in range(len(response['items'][0]['bestKeyword'])):
            keyword = response['items'][0]['bestKeyword'][j]['keyword']
            print(f"{count}. {keyword}")
            pandarank_keyword_lists.append(keyword)
            count = count + 1

    # df = pd.DataFrame()
    # df['keyword'] = pandarank_keyword_lists
    
    df = pd.DataFrame(pandarank_keyword_lists, columns=['keyword'])
    if not os.path.exists(keyword_csv_file_path):
        df.to_csv(keyword_csv_file_path, mode='w', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False)
    else:
        df.to_csv(keyword_csv_file_path, mode='a', sep=',', na_rep='NaN', encoding='utf-8-sig', index=False, header=False)

    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀 ({keyword_csv_file_path}) 행을 제거 시작{C_END}')
    data = pd.read_csv(keyword_csv_file_path)
    data = data.drop_duplicates(subset=['keyword'], keep="first")
    data.to_csv(keyword_csv_file_path, index=False, encoding="utf-8-sig")
    print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}중복된 검색 결과의 엑셀행 제거 및 저장 완료{C_END}\n')


# main start
def main():
    try:
        start_time = time.time()  # 시작 시간 체크
        now = datetime.datetime.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        print("\nSTART...")
        
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[판타랭크 정보 가져오기 시작(keyword 추출)]', C_END)
        get_keyword_pandarank()
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[판타랭크 정보 가져오기 완료]', C_END)
    
    finally:
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(datetime.timedelta(seconds=ctime)).split(".")
        print(f"\n실행시간 (시:분:초)", time_list)
        now = datetime.datetime.now()
        print("END TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        print("\nEND...")
# main end


if __name__ == '__main__':
    main()

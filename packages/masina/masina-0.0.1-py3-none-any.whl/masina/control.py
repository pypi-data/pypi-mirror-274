from datetime import date
import masina


def get_auto_vals(ini_file, selectedStartDate, selectedEndDate):
    auto = masina.Masina(ini_file)
    alimentari = auto.get_alimentari_for_interval_type(selectedStartDate, selectedEndDate, None)
    for i in alimentari:
        print(i)
    # print(auto.table_totals)


def main():
    selectedStartDate = date(2021, 12, 30)
    selectedEndDate = date(2024, 1, 29)

    income_ini = r"D:\Python\MySQL\cheltuieli_db.ini"
    get_auto_vals(income_ini, selectedStartDate, selectedEndDate)

if __name__ == '__main__':
    main()

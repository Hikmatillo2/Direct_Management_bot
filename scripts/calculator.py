class Calculator:
    def __init__(self, clicks: int, money: int, site: float = 0.03, manager: float = 0.1, traffic: float = 0.62):
        self.SITE = site
        self.MANAGER = manager
        self.TRAFFC = traffic
        self.clicks = clicks
        self.money = money

    def per_day_without_nds(self):
        return round((self.money * 1.2) / (self.clicks * self.SITE) * (self.clicks * self.TRAFFC * self.SITE) / 31)

    def per_day_with_nds(self):
        return round(self.per_day_without_nds() * 1.2)

    def lead_without_nds(self):
        return round((self.money * 1.2) / (self.clicks * self.SITE))

    def lead_with_nds(self):
        return round(1.2 * self.lead_without_nds())

    def one_week_with_nds(self):
        return round(
            7 * 1.2 * (self.money * 1.2) / (self.clicks * self.SITE) * (self.clicks * self.TRAFFC * self.SITE) / 31)

    def orders_per_week(self):
        return round((7 * self.TRAFFC * self.SITE * self.clicks) / 31)

    def sales_per_week(self):
        return round((7 * self.TRAFFC * self.SITE * self.MANAGER * self.clicks) / 31)

    def conversions_per_month(self):
        return round(4 * self.orders_per_week())

    def compile(self, stgs: bool = False):
        if stgs:
            return {0: ['Прогноз расхода в день без ндс', 'Стоимость лида 1 шт. без ндс', 'Кол-во заявок за неделю'],
                    1: [self.per_day_without_nds(), self.lead_without_nds(), self.orders_per_week()],
                    2: ['Прогноз расхода в день с ндс', 'Стоимость лида 1 шт. с ндс', 'Кол-во продаж за неделю'],
                    3: [self.per_day_with_nds(), self.lead_with_nds(), self.sales_per_week()],
                    4: ['Кол-во Рекламного бюджета на одну неделю с НДС', '', 'Кол-во конверсий за месяц'],
                    5: [self.one_week_with_nds(), '', self.conversions_per_month()]}, \
                   f'Исходные данные:\nклики - {self.clicks}\nбюджет - {self.money}\n' \
                   f'конверсия сайта - {self.SITE * 100}%\nэффективность менеджера - {self.MANAGER * 100}%\n' \
                   f'трафик - {self.TRAFFC * 100}%'
        return {0: ['Прогноз расхода в день без ндс', 'Стоимость лида 1 шт. без ндс', 'Кол-во заявок за неделю'],
                1: [self.per_day_without_nds(), self.lead_without_nds(), self.orders_per_week()],
                2: ['Прогноз расхода в день с ндс', 'Стоимость лида 1 шт. с ндс', 'Кол-во продаж за неделю'],
                3: [self.per_day_with_nds(), self.lead_with_nds(), self.sales_per_week()],
                4: ['Кол-во Рекламного бюджета на одну неделю с НДС', '', 'Кол-во конверсий за месяц'],
                5: [self.one_week_with_nds(), '', self.conversions_per_month()]}

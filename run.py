import fire
import pandas as pd
from bs4 import BeautifulSoup

def create_total_column(df: pd.DataFrame, col: str) -> None:
    """Filter out bad characters and create cash col for input column"""
    df[f'{col}_cash'] = df[df[col] == True]['amount']
    df[f'{col}_cash'] = df[f'{col}_cash'].replace(',', '', regex=True)
    df[f'{col}_cash'] = df[f'{col}_cash'].replace('\+', '', regex=True)
    df[f'{col}_cash'] = df[f'{col}_cash'].replace('\-', '', regex=True)
    df[f'{col}_cash'] = df[f'{col}_cash'].replace('Failed', '0', regex=True)
    df[f'{col}_cash'] = df[f'{col}_cash'].replace('Canceled', '0', regex=True)
    df[f'{col}_cash'] = df[f'{col}_cash'].replace('\$', '', regex=True).fillna(0)
    df[f'{col}_cash'] = df[f'{col}_cash'].astype(float)

def extract_metrics(file_location: str) -> None:
    """takes an html file loation and prints metrics"""
    soup = BeautifulSoup(open(file_location), "html.parser")
    robinhood = soup.find_all('div', {'class' : "_2VPzNpwfga_8Mcn-DCUwug"})
    body = list(soup.children)[4]
    div_list = list(body.children)[2]
    div_list2 = list(div_list)[1]
    titles = []
    amount = []
    for x in list(soup.find_all('div', {'class': "_3znyYq5FdX98HAPHPumJG1"})):
        for ind, element in enumerate(x):

            if ind == 0:
                titles.append(list(element.find_all("h3"))[0].getText())
            else:
                amount.append(list(element.find_all("h3"))[0].getText())

    df = pd.DataFrame({'titles':titles, 'amount': amount})
    pd.set_option('display.max_rows', df.shape[0]+1)

    df['dividend'] = df['titles'].str.contains('Dividend from', regex=False)
    create_total_column(df,'dividend')

    df['deposit'] = df['titles'].str.contains('Deposit from', regex=False)
    create_total_column(df,'deposit')

    df['gold'] = df['titles'].str.contains('Robinhood Gold', regex=False)
    create_total_column(df,'gold')

    df['withdrawal'] = df['titles'].str.contains('Withdrawal', regex=False)
    create_total_column(df,'withdrawal')
    total_dividends_earned = sum(df['dividend_cash'])
    total_deposited_cash = sum(df['deposit_cash'])
    total_gold_spent = sum(df['gold_cash'])
    total_withdrawal = sum(df['withdrawal_cash'])

    print(f'Total Dividends Earned: {total_dividends_earned}')
    print(f'Total Deposited Cash: {total_deposited_cash}')
    print(f'Total Withdrawn Cash: {total_withdrawal}')
    print(f'Total spent on Robinhood Gold: {total_gold_spent}')

if __name__ == '__main__':
  fire.Fire(extract_metrics)


""" Currently Unused, May be in the future
    df['buy_call_buy'] = df['titles'].str.contains('Buy', regex=False)
    df['buy_call_call'] = df['titles'].str.contains('Call', regex=False)
    df['buy_call'] = df['buy_call_buy'] & df['buy_call_call']
    create_total_column(df,'buy_call')
    df['sell_call_sell'] = df['titles'].str.contains('Sell', regex=False)
    df['sell_call_call'] = df['titles'].str.contains('Call', regex=False)
    df['sell_call'] = df['sell_call_sell'] & df['sell_call_call']
    create_total_column(df,'sell_call')
"""
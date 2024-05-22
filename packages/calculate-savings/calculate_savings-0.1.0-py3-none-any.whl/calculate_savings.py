import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression
import pkg_resources


def calculate(living_expenses, discretionary_spending):
    # csv_path = pkg_resources.resource_filename("src", "data/hon-maikin-k-jissu.csv")
    # df = pd.read_csv(csv_path, encoding="Shift JIS")

    # filtered_df = df[df["産業分類"] == "TL  "]
    # filtered_df = filtered_df[filtered_df["就業形態"] != 2]
    # new_df = filtered_df[["年", "現金給与総額"]]

    # # 規模別に対してその年の平均をとる
    # df = new_df.groupby("年", as_index=False)["現金給与総額"].mean()

    # data = df["現金給与総額"].tolist()
    # start = datetime(df["年"][0], 1, 1).strftime("%Y-%m-%d")
    # end = datetime(df["年"].iloc[-1], 12, 31).strftime("%Y-%m-%d")
    # date = pd.date_range(start=start, end=end, freq="Y")

    # 出典：「毎月勤労統計調査」
    data = [
        76435.25,
        87696.5,
        101672.15384615384,
        123709.63461538461,
        156727.34615384616,
        179431.21153846153,
        203095.25,
        222198.01923076922,
        238255.36538461538,
        251612.88461538462,
        268486.4423076923,
        284307.42307692306,
        294676.6538461539,
        304267.9423076923,
        317634.23076923075,
        324772.03846153844,
        333424.5,
        342343.23076923075,
        351756.6538461539,
        368306.01923076925,
        354326.46153846156,
        369352.92307692306,
        377015.8205128205,
        397440.74358974356,
        405007.8717948718,
        412437.2756410256,
        417554.28205128206,
        426987.3205128205,
        422652.0641025641,
        412708.03205128206,
        415925.1346153846,
        414624.608974359,
        408040.25641025644,
        409083.82692307694,
        403877.73076923075,
        407149.4487179487,
        409534.53205128206,
        403225.3717948718,
        404101.41025641025,
        381652.07692307694,
        387163.0448717949,
        388684.75641025644,
        384037.01923076925,
        386211.67307692306,
        391473.50641025644,
        387157.6346153846,
        390490.2948717949,
        392195.5128205128,
        397819.4551282051,
        397348.76923076925,
        390539.9743589744,
        392890.4166666667,
        402812.8076923077,
        409031.91025641025,
        338986.6666666667,
    ]
    date = pd.date_range(start="1970-01-01", end="2024-12-31", freq="Y")

    df = pd.DataFrame(data, index=date, columns=["Salary"])

    # 線形回帰モデルを使って将来の値を予測
    years_to_predict = 10
    future_dates = pd.date_range(
        start=df.index[-1], periods=years_to_predict + 1, freq="Y"
    )[
        1:
    ]  # 最後の日から10年後までの日付
    X = df.index.year.values.reshape(-1, 1)  # インデックスから年を抽出
    y = df["Salary"]

    model = LinearRegression()
    model.fit(X, y)

    future_X = future_dates.year.values.reshape(-1, 1)
    future_y = model.predict(future_X)

    # 10年後までの貯金を計算
    savings = 0
    for projected_income in future_y:
        savings += projected_income - (living_expenses + discretionary_spending)
        print(
            f"{savings} = {projected_income} - {living_expenses} - {discretionary_spending}"
        )

    # プロット
    plt.figure(figsize=(12, 8))

    # 実際の賃金データをプロット
    plt.plot(df.index, df["Salary"], label="Actual Data", color="blue")

    # 給料の予測値をプロット
    plt.plot(future_dates, future_y, "r--", label="Predicted Data")

    # 10年後までの貯金額を表示
    plt.text(
        future_dates[-1],
        future_y[-1],
        f"Savings: {savings:.2f}",
        verticalalignment="bottom",
        horizontalalignment="right",
        color="green",
        fontsize=12,
    )

    plt.title("Salary prediction and savings calculation")
    plt.xlabel("Year")
    plt.ylabel("Salary")
    plt.legend()
    plt.grid(True)
    plt.show()

    return savings


def main():
    # Asking the user for living expenses and discretionary spending
    try:
        living_expenses = float(input("Enter your living expenses for 1 year: "))
        discretionary_spending = float(
            input("Enter your discretionary spending for 1 year: ")
        )
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    # Calculating savings
    savings = calculate(living_expenses, discretionary_spending)
    print("Savings till 10 years(yen): ", savings)

    # Saving the graph
    plt.savefig("result.png")
    plt.show()


if __name__ == "__main__":
    main()

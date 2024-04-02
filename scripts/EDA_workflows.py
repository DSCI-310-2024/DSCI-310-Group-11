import numpy as np
import pandas as pd
import altair as alt
import os
import click
import sys
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.eda_functions import * 
from src.data_clean_functions import * 

alt.data_transformers.enable("vegafusion")
alt.renderers.enable('jupyterlab')
alt.renderers.enable('mimetype')

@click.command()
@click.option('--parquet_path', type=str, help = 'File path of train data', default='../data/cricket_main.parquet')
@click.option('--save_path', type=str, help = 'File path to save image outputs', default='../images')
@click.option('--save_table_path', type=str, help = 'File path to save table outputs', default='../data/data_for_quarto')

def main(parquet_path, save_path, save_table_path):
    
    data = pd.read_parquet(parquet_path)
    X, y = separate_columns(data)
    X_train, X_test, y_train, y_test, train_data = split_and_save_data(X, y, train_size=0.7, save_table_path="../data/data_for_quarto")


    over = vis_bar(data, "over", 150, 150)
    wides = vis_bar(data, "wides", 150, 150)
    noballs = vis_bar(data, "noballs", 150, 150)
    legbyes = vis_bar(data, "legbyes", 150, 150)
    byes = vis_bar(data, "byes", 150, 150)
    wicket = vis_bar(data, "wicket", 150, 150)
    run_batter = vis_bar(data, "runs_batter", 150, 150)
    run_extras = vis_bar(data, "runs_extras", 150, 150)
    run_total = vis_bar(data, "runs_total", 150, 150)
    over_ball = vis_bar(data, "over_ball", 150, 150)
    runs_cumulative = vis_bar(data, "runs_cumulative", 150, 150)

    title_1_a = alt.Chart(
        {"values": [{"text": "Figure 1.1: Distribution of Variables"}]}
    ).mark_text(size=20).encode(
        text="text:N"
    )
    
    v1 = alt.hconcat(over, wides, noballs)
    v2 = alt.hconcat(legbyes, byes, wicket)
    v3 = alt.hconcat(run_batter, run_extras, run_total)
    v4 = alt.hconcat(over_ball, runs_cumulative)
    chart1 = alt.vconcat(v1, v2, v3, v4)
    chart1.save(os.path.join(save_path, "chart1.png"))

    season = vis_bar(data, "season", 500, 150)
    team = vis_bar(data, "team", 900, 150)
    inning = vis_bar(data, "inning:N", 150, 150)
    powerplay = vis_bar(data, "powerplay:N", 150, 150)

    title_1_b = alt.Chart(
        {"values": [{"text": "Figure 1.2: Distribution of Variables"}]}
    ).mark_text(size=20).encode(
        text="text:N"
    )

    h_1 = alt.hconcat(inning, powerplay)
    chart2 = alt.vconcat(season, team, h_1)
    chart2.save(os.path.join(save_path, "chart2.png"))

    corr_data = data[["over", "wides", "noballs", "legbyes", "byes", "runs_batter", "runs_extras", "runs_total", "over_ball", "runs_cumulative", "wicket"]]
    corr_df = corr_data.corr()
    corr_df.style.set_caption("Table 4: Correlation Analysis").set_table_styles([{
        'selector': 'caption',
        'props': 'caption-side: bottom; font-size:1.25em;'
    }], overwrite=False)

    corr_ = corr_df.stack()
    corr_ = corr_.reset_index()
    corr_.columns = ['row', 'column', 'corr']

    chart3 = alt.Chart(corr_).mark_rect().encode(
        x = 'column',
        y = 'row',
        color = 'corr:Q',
        tooltip = 'corr:Q'
    ).properties(
        width = 400,
        height = 400
    )
    chart3.save(os.path.join(save_path, "chart3.png"))

    hist_chart(data, 'over', 'chart4.png', save_path)
    hist_chart(data, 'inning', 'chart5.png', save_path)
                
    # over_count_wicket = data.groupby('over')['wicket'].count()
    # chart4 = over_count_wicket.plot(kind = 'bar', xlabel="Over", ylabel="Wicket Count")
    # fig4 = chart4.get_figure()
    # fig4.savefig(os.path.join(save_path, "chart4.png"))

    # inning_count_wicket =  data.groupby('inning')['wicket'].count()
    # chart5 = inning_count_wicket.plot(kind = 'bar', xlabel ='inning', ylabel = 'Wicket Count')
    # fig5 = chart5.get_figure()
    # fig5.savefig(os.path.join(save_path, "chart5.png"))

    data_0 = data[data['wicket'] == 0]
    data_1 = data[data['wicket'] == 1]

    plt.figure()
    plt.hist(data_0['runs_cumulative'],  
            label="Not a Wicket",
            alpha = 0.5, 
            density = True) 
    
    plt.hist(data_1['runs_cumulative'],  
            label="Wicket",
            alpha = 0.5,
            density=True) 
    
    plt.legend(loc='upper right') 
    plt.xlabel("Runs scored until Current Ball in Current Innings")
    plt.ylabel("Probability Density")
    plt.savefig(os.path.join(save_path, "chart6.png"), bbox_inches='tight')

if __name__ == '__main__':
    main()
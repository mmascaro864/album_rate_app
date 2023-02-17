import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `album_rate_app/data/file_name.csv`

def rename_cols(df):
    '''
    rename_cols: rename columns to lower case, changing spaces to underscores
    
    Args: 
      dataframe
    
    Returns: 
      dataframe
    '''
    df.columns = [i.replace(' ', '_').lower() for i in df.columns]
    
    return(df)

def cleandata(dataset):
    '''
    Clean Rate Your Album data for a visualization dashboard

    Args:
      dataset (str): name of csv data file
  
    Returns:
      None
  
    '''

    df = pd.read_csv(dataset, index_col = False)

    # change column names to lowercase and replace spaces with underscore
    rename_cols(df)

    # update datatypes
    # for number_of_ratings, first remove comma
    df['number_of_ratings'] = df['number_of_ratings'].str.replace(',', '')
    df['number_of_ratings'] = df['number_of_ratings'].astype('int64')

    # change release_date to datetime 
    df['release_date'] = pd.to_datetime(df['release_date'])

    # delete unneeded columns
    df = df.drop(columns = ['descriptors'], axis = 1)

    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # load data
    df = cleandata('album_rate_app/data/rym_top_5000_all_time.csv')

    # we'll look at the top 10 ranked albums as of 2021,
    # so will take a subset of the data

    top_ranked_albums = df.query('ranking >= 1 & ranking <=10')

    # initialize graph_one list

    graph_one = [] 

    # define graph_one - top 10 ranked albums as of 2021

    graph_one.append(
        go.Bar(
            y = top_ranked_albums.album,
            x = top_ranked_albums.ranking,
            orientation = 'h',
            text=top_ranked_albums.artist_name,
            marker = dict(
                    line=dict(
                        width=2,
                        color='white'
                        )
                    )
          )
        )

    # define layout_one 

    layout_one = dict(title = 'Top 10 Ranked Albums of All Time (as of 2021)',
                xaxis_title = 'Ranking',
                yaxis_title = 'Album Name',
                xaxis = dict(
                    tickmode = 'linear',
                    tick0 = 0,
                    dtick = 1.0
                    )
                )

    # initialize graph_two list

    graph_two = [] 

    # define graph_two - the top 10 ranked albums by release date 

    graph_two.append(
        go.Scatter(
            y=top_ranked_albums.album,
            x=top_ranked_albums.release_date,
            mode='markers',
            text=top_ranked_albums['artist_name'],
            marker=dict(size=12, 
                        line=dict(width=2, 
                                  color='white'
                                )
                      )
        )
    )

    # define layout_two

    layout_two = dict(title = 'Top 10 Ranked Albums of All Time (as of 2021) by Year Released',
                      xaxis_title = 'Year Released',
                      yaxis_title = 'Album Name'
                    )

    # for the third graph, we want to find the artists with the most ranked albums,
    # so we will subset the data 

    most_ranked_artists = df.artist_name.value_counts().nlargest(10) # take the top 10 artists
    most_ranked_artists.to_frame().reset_index(drop = True, inplace = True) # create dataframe from list

    # initialize graph_three

    graph_three = []

    # define graph_three - artists with the most ranked albums

    graph_three.append(
        go.Bar(
            y=most_ranked_artists,
            x=most_ranked_artists.index,
            text=most_ranked_artists
        )
    )

    # define layout_three

    layout_three = dict(title = 'Artists with most ranked albums (as of 2021)',
                        xaxis_title = 'Artist',
                        yaxis_title = 'Count'
                      )
    
    # initialize graph_four

    graph_four = []

    # define graph_four

    graph_four.append(
        go.Bar(
            x = df.album,
            y = df.average_rating.nlargest(10),
            text = df.artist_name,
            textposition = 'top left',
            marker = dict(line = dict(width = 2,
                                      color='white'))
            )
    )

    # define layout_four

    layout_four = dict(title = 'Albums with highest average ratings - Top 10 (as of 2021)',
                      xaxis_title = 'Album',
                      yaxis_title = 'Rating',
                      yaxis = dict(tickmode = 'linear',
                                  tick0 = 0.0,
                                  dtick = 0.5
                                  )
    )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
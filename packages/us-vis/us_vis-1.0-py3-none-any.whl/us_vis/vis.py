import matplotlib.pyplot as plt
import itertools


def col_names(data):
    """
    Since naming of the columns does not need to the same 
    the code here names columns in unified way.
    """
    column_names = []
    work_columns = []
    j = 10
    for i in range(1, (data.shape[1] + 1)):
        if i == 1:
            column_names.append("Coord")
        elif (i % 2) == 0:
            column_names.append("US" + str(j))
            work_columns.append("US" + str(j))
            j += 10
        elif (i % 2) == 1:
            column_names.append("")
    data.columns = column_names
    return data, work_columns


def sub_min(data, work_columns):
    """
    
    """
    for i in work_columns:
        new_col = []
        for j in data[i]:
            k = j-data[(data["Coord"] >= 2.0)][i].min()
            new_col.append(k)
        data[i] = new_col
    return data


def vis_fun(data, work_columns, name):
    """
    Visualization of the data
    """
    Ncolors = len(work_columns) # Defining how many colors should there be
    colormap = plt.cm.Set3  # Choosing colormaps
    mapcolors = [colormap(int(x*colormap.N/Ncolors)) for x in range(Ncolors)]
    l_styles = ['-']  # If in the future I want to change linestyle
    m_styles = ['']  # If in the future I want to add marker
    fig, ax = plt.subplots(gridspec_kw=dict(right=0.85)) 
    for i, (marker, linestyle, color) in zip(work_columns,
                                             itertools.product(m_styles,
                                                               l_styles,
                                                               mapcolors)):
        ax.plot(data["Coord"], data[i], color=color, linestyle=linestyle,
                marker=marker, label=i)
    plt.xlim(1.4, 3.5)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    plt.title(name)
    fig.legend(loc="right", ncol=1, prop={'size': 8})


def vis_show(data, work_columns, name):
    """
    Showing the figure
    """
    vis_fun(data, work_columns, name)
    plt.show()


def vis_save(data, work_columns, name):
    """
    Saving picture as .png
    """
    vis_fun(data, work_columns, name)
    plt.savefig(name+".png")


def odd_col(data, work_columns):
    """
    Function that finds incorrect runs
    """
    odd_out = []
    for i in work_columns:
        odd = []
        for j in range(1, len(data[(data["Coord"] >= 2.5)][i])):
            if data[(data["Coord"] >= 2.0)
                   ].loc[j+14, i] > data[(data["Coord"] >= 2.0)
                                        ].loc[j+14-1, i]:
                odd.append("1")
        if len(odd) > 10:
            odd_out.append(i)
            print(f"You might need to recalculate {i}")
    return odd_out


def split_strings(list_strings):
    """
    Function that splits string into list
    """
    list_strings = list_strings.split(" ")
    return list_strings


def del_col(work_columns, columns):
    """
    Mostly used with user input - function creates the list of runs 
    without the ones that are mentioned in "columns"
    """
    delete_columns = split_strings(columns)
    delete_columns = ["US"+str(eval(i)*10) for i in delete_columns]
    work_columns = [i for i in work_columns if i not in delete_columns]
    return work_columns


def spread(data, odd_out):
    """
    Function calculates if the spread (the difference between the maximum
    and minimum of energy in the product side) is smaller than 20
    """
    min = data[(data["Coord"] <= 2.0)].loc[5, "US10"].min()
    max = data[(data["Coord"] <= 2.0)].loc[5, "US10"].max()
    for i in [i for i in list(data.columns.values) if i not in odd_out]:
        new_min = data[(data["Coord"] <= 2.0)].loc[5, i].min()
        new_max = data[(data["Coord"] <= 2.0)].loc[5, i].max()
        if new_min < min:
            min = new_min
        if new_max > max:
            max = new_max
        diff = max-min
    if diff > 20:
        print("The spread is high")

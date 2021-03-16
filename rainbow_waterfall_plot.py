import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import constants.currentConstants as c
import os

#data iss structures as an array of arrays of form [gen, fitness, age] 
def update_color(color):
    """update color. Using matplotlib default colors (C0, C1, ..., C9), select the next
    one in the list. If at C9, go to C0. Thus, if more than 10 colors are needed, there
    will be duplicates."""

    num = int(color[-1])

    return 'C'+str((num+1) % 10)


def rainbow_waterfall_plot_old(max_gens, min_gens, save_loc=None, colors=None):
    """Visualization tool for AFPO (mutliple file version).
    Color individuals from the
    same lineage the same. Connect the best (lowest error) individuals
    from each lineage of the past generation to the best individuals
    in the current generation.

    max_gens: number of generations at which to stop plotting
    min_gens: number of generations at which to start plotting. Default is 0.
    save_loc (optional): filepath at which final image should be save. If None, show image
    colors (optional): Dictionary of colors where key=lineage (generation-age) and
    value=color (string). Colors must be one of (C0, C1, ..., C9). If None, first lineage found
    will get C0, second will get C1, and so on."""

    if colors is None:

        colors = {}  # key=lineage, value=color
        next_color = 'C0'

    else:

        # find first "free" color and assign it as next_color
        color_numbers = [int(colors[lin][-1]) for lin in colors]
        next_color = 'C0'

        for i in range(10):

            if i not in color_numbers:

                next_color = ''.join(['C', str(i)])
                break

    prev_best = {}
    stop = False

    plt.figure(dpi=400)
    ax = plt.subplot(111)

    # When turned on, these setting slow down plotting
    ax.autoscale(False)
    ax.use_sticky_edges = False

    for gen in range(min_gens, max_gens):

        print('.', end='', flush=True)

        file = os.path.join(path, 'pop_data_gen%06d.csv' % gen)

        try:

            df = pd.read_csv(file)

        except FileNotFoundError:

            print('Could not find', file)
            print('Stopping!')
            stop = True
            break

        errors = df.iloc[:, 2].values
        ages = df.iloc[:, 4].values

        lineages = gen - ages

        # if there are dead lineages, they don't need a color
        keys_to_delete = [key for key in colors if key not in np.unique(lineages)]

        for key in keys_to_delete:

            del colors[key]

        best = {}

        for i, lin in enumerate(np.unique(lineages)):

            if lin not in colors:

                colors[lin] = next_color
                next_color = update_color(next_color)

            indices = np.where(lineages==lin)

            best[lin] = np.min(errors[indices])

            if lin in prev_best:

                plt.plot([gen-1, gen], [prev_best[lin], best[lin]], colors[lin], ms=1, alpha=0.9)

        prev_best = best

    plt.ylim(bottom=0,top=10)#(bottom=10**(-1), top=10**3)
    plt.xlim([min_gens, max_gens])

    ax.set_yscale(10)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.title('Rainbow Waterfall Plot')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')

    plt.tight_layout()

    if save_loc:

        directory = os.path.dirname(save_loc)

        if not os.path.exists(directory):

            os.mkdir(directory)

        plt.savefig(save_loc)

    else:

        plt.show()

    return colors, stop


def rainbow_waterfall_plot(data, max_gens, min_gens=0, save_loc=None, colors=None):
    """Visualization tool for AFPO. Color individuals from the
    same lineage the same. Connect the best (lowest error) individuals
    from each lineage of the past generation to the best individuals
    in the current generation.

    data: input data
    max_gens: number of generations at which to stop plotting
    min_gens: number of generations at which to start plotting. Default is 0.
    save_loc (optional): filepath at which final image should be save. If None, show image
    colors (optional): Dictionary of colors where key=lineage (generation-age) and
    value=color (string). Colors must be one of (C0, C1, ..., C9). If None, first lineage found
    will get C0, second will get C1, and so on."""

    if colors is None:

        colors = {}  # key=lineage, value=color
        next_color = 'C0'

    else:

        # find first "free" color and assign it as next_color
        color_numbers = [int(colors[lin][-1]) for lin in colors]
        next_color = 'C0'

        for i in range(10):

            if i not in color_numbers:

                next_color = ''.join(['C', str(i)])
                break

    prev_best = {}

    plt.figure(dpi=400)
    ax = plt.subplot(111)

    # When turned on, these setting slow down plotting
    ax.autoscale(False)
    ax.use_sticky_edges = False

    for gen in range(min_gens, max_gens):
        if gen ==  100:
            print("HI")
        print('.', end='', flush=True)

        # assume 100 individuals per gen
        errors = data[gen*c.popSize:(gen+1)*c.popSize, 2]
        ages = data[gen*c.popSize:(gen+1)*c.popSize, 3]
        
        lineages = gen - ages

        # if there are dead lineages, they don't need a color
        keys_to_delete = [key for key in colors if key not in np.unique(lineages)]

        for key in keys_to_delete:

            del colors[key]

        best = {}

        for i, lin in enumerate(np.unique(lineages)):

            if lin not in colors:

                colors[lin] = next_color
                next_color = update_color(next_color)

            indices = np.where(lineages==lin)

            best[lin] = np.max(errors[indices])

            if lin in prev_best:

                plt.plot([gen-1, gen], [prev_best[lin], best[lin]], colors[lin], ms=1, alpha=0.9)

        prev_best = best

    plt.ylim(bottom=0, top = 2) #(bottom=10**(-1), top=10**3)
    plt.xlim([min_gens, max_gens])

    #ax.set_yscale(10)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.title('Rainbow Waterfall Plot')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')

    plt.tight_layout()

    if save_loc:

        directory = os.path.dirname(save_loc)

        if not os.path.exists(directory):

            os.mkdir(directory)

        plt.savefig(save_loc)

    else:

        plt.show()

    return colors


if __name__ == '__main__':

    # # old version (multiple files)
    # project_path = 'primitive_set_transitions/experiments'
    # exp_path = '135/RatPol3D/PD0_AQ1_CD0_AQs0_TP0_CDs0_A0_E0_ST0_FGU0/pop/0'
    #
    # path = os.path.join(os.environ['GP_DATA'], project_path, exp_path)
    #
    # print(path)
    #
    # max_gens = 5000
    # colors = None
    #
    # for offset in range(10):
    #     print('offset', offset, end='')
    #
    #     save_loc = os.path.join(path, 'images',
    #                             'rainbow_waterfall_plot_'+exp_path.replace('/', '-')+'_offset'+str(offset)+'.png')
    #
    #
    #     colors, stop = rainbow_waterfall_plot_old(max_gens*(offset+1), min_gens=max_gens*offset,
    #                                               colors=colors, save_loc=save_loc)
    #
    #     print('')
    #
    #     if stop:
    #         print('Stop')
    #         break


    # new version (single file for all individuals)
    rep = 0

    project_path = 'primitive_set_transitions/experiments'
    exp_path = '200/RatPol3D/PD1_AQ0_CD0_AQs0_TP0_CDs0_A0_E0_ST0_FGU0'

    #path = os.path.join(os.environ['GP_DATA'], project_path, exp_path)
    path = 'rainbow.csv'
    print(path)

    #filepath = os.path.join(path, 'pop_data_rep'+str(rep)+'.csv')
    filepath = path
    data = pd.read_csv(filepath).iloc[:, :].values
    min_gens = 0
    max_gens = 200

    save_loc = os.path.join('images', 'rainbow_waterfall_plot_new'+'.png')
    

    colors = rainbow_waterfall_plot(data, max_gens, min_gens, save_loc=save_loc)

    print('')

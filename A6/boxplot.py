import matplotlib.pyplot as plt

# Define lists to store the health and gold values
health = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': []}
gold = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [], 'i': []}


# Read the file
with open('test.txt', 'r') as file:
    read_players = False
    line = file.readline()
    while line:
        # Skip the lines until the player data starts
        if line.startswith('Player   Health   Gold      Position'):
            print(f'We read {line} in first if')
            read_players = True
            line = file.readline()

        if line.startswith('Gold Pots:'):
            print(f'We read {line} in second if')
            read_players = False
            line = file.readline()


        # Process player data
        if read_players:
            print(f'We read {line}')
            line = line.strip()

            player_data = line.split()
            if len(player_data) == 4:
                print(player_data)
                player = player_data[0]
                player_health = int(player_data[1])
                player_gold = int(player_data[2])
                health[player].append(player_health)
                gold[player].append(player_gold)
            else:
                print('No line read!')
        line = file.readline()


# Print the health and gold lists
print("Health List:", len(health['a']), health)
print("Gold List:", len(gold['a']), gold)

import matplotlib.pyplot as plt

player_labels = {'a': 'AStarScout', 'b': 'Another AStarScout', 'c': 'FabioPfae_GoodBot', 'd': 'GandolfTheWhite',
                 'e': 'lmiksch_test', 'f': 'Aggressive Drifter', 'g': 'Established Drifter', 'h': 'GutKat', 'i': 'YEEEEET'}

# Extract player names and health/gold values from the data dictionaries
players = list(health.keys())
health_values = list(health.values())
gold_values = list(gold.values())

# Set up subplots for health, gold boxplots, violin plots, and legend
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))

# Create boxplots for health values in the first subplot
axes[0, 0].boxplot(health_values, patch_artist=True)
axes[0, 0].set_ylabel('Health')
axes[0, 0].grid(axis='y', which='major')
axes[0, 0].set_title('Health Boxplot')
# Remove x-ticks and labels for the first subplot
axes[0, 0].xaxis.set_ticks_position('none')
axes[0, 0].get_xaxis().set_visible(False)

# Create boxplots for gold values in the second subplot
colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'brown', 'gray', 'olive']
boxplot = axes[0, 1].boxplot(gold_values, patch_artist=True)
axes[0, 1].set_ylabel('Gold')
axes[0, 1].grid(axis='y', which='both')
axes[0, 1].set_title('Gold Boxplot')
# Remove x-ticks and labels for the second subplot
axes[0, 1].xaxis.set_ticks_position('none')
axes[0, 1].get_xaxis().set_visible(False)

# Assign colors to boxplots for each player in the first two subplots
for i, box in enumerate(boxplot['boxes']):
    box.set_facecolor(colors[i])

# Add violin plots of the gold values to the third subplot
violin_parts = axes[1, 0].violinplot(gold_values, showmedians=True, showextrema=False)
for idx, pc in enumerate(violin_parts['bodies']):
    pc.set_facecolor(colors[idx])

axes[1, 0].set_ylabel('Gold')
axes[1, 0].grid(axis='y', which='both')
axes[1, 0].set_title('Gold Violin Plot')

# Create a legend on the fourth subplot
legend_labels = [player_labels[player] for player in players]
legend_patches = [plt.Rectangle((0, 0), 1, 1, facecolor=colors[i]) for i in range(len(players))]
legend = axes[1, 1].legend(legend_patches, legend_labels, loc='center', prop={'size': 12})
legend.set_title("Legend", prop={'size': 14})
axes[1, 1].axis('off')
# Adjust spacing between subplots
fig.suptitle('Results for 200 runs of length 100', fontsize=16, fontweight='bold')
plt.tight_layout()

# Display the plot
plt.show()

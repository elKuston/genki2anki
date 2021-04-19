# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import easyocr


# %%
images_path = 'images/'


# %%
image = images_path+'ru-verbs.png'


# %%
reader = easyocr.Reader(['en', 'ja'])
read = reader.readtext(image)


# %%
def coord_esquinas_centrales_palabra(palabra):
    return [esquina[1] for esquina in palabra[0]][1:3]

def group_words_by_row(read_data):
    words = [r[1] for r in read_data]
    rows = []
    curr_row = []
    last_y = coord_esquinas_centrales_palabra(read_data[0])
    last_center = (last_y[0] + last_y[1])/2
    for r in read:
        curr_y = coord_esquinas_centrales_palabra(r)
        epsilon = (0.1 + 0.5) * (last_y[1] - last_y[0])
        curr_center = (curr_y[0] + curr_y[1])/2
        if curr_center <= last_center-epsilon or curr_center  >= last_center+epsilon:  # If it's not within +-10% of the row y, then its a new row
            rows.append(curr_row)
            curr_row = []
        curr_row.append(r[1])
        last_center = curr_center
        #print(r)
        #print(last_y)
        #print(r[1], r[2])
    rows.append(curr_row)
    return rows


# %%
rows = group_words_by_row(read)
rows


# %%
def get_cards(rows):
    cards = []
    for w in rows:
        front = None
        if len(w) == 2:
            front = w[1]
            back = w[0]
        elif len(w) == 3:
            front = w[2]
            back = w[1] +'  '+ w[0]
        if front is not None:
            cards.append([front, back])
        else:
            print('Discarded row: '+w)
    return cards


# %%
cards = get_cards(rows)
cards


# %%
def export(cards, filename):
    f = open(filename,'w', encoding='utf-8')
    for c in cards:
        text = c[0]+'\t'+c[1]+'\n'
        f.write(text)

    f.close()


# %%
export(cards, 'demo_deck.csv')


# %%



# %%




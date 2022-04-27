# IR2022_Project_8

![alt text](https://github.com/AbhinavSE/IR2022_Project_8/blob/master/App/assets/1.png?raw=true)

## Steps to add dataset
- Download songs folder from this [link](https://drive.google.com/drive/folders/1lXHVGBgL0FvHOf4Ao_TrrSPdvhRq-iwq?usp=sharing)
- Add the songs folder to Apps/Assets/Data folder
- Keep the folder name to 'songs'

## How to Run
    pip install requirements.txt
    cd App
    python run.py```

- App should be up at ```http://127.0.0.1:8050```

## How to Use

- The UI is straight-forward as seen in the below image

    <img width="1675" alt="Screen_Shot_2022-04-27_at_10 14 11_PM" src="https://user-images.githubusercontent.com/56074469/165583307-003b628a-c3b3-4c0f-8545-1ea50318e13a.png">

    The cards represent the songs in our database. There are around 400 songs where each card has a title and artist of the song. There is also a play and like button. The play button, when pressed, plays the song in the player frozen in the bottom pane. The player has an option to play/pause and even scrub the song in real time.

- Above the cards, there is a search bar, where you can search songs based on three values: Title, artist and by lyrics too. While typing, the cards below are updated in real time based on the suggestions. 

    <img width="1674" alt="Screen_Shot_2022-04-27_at_10 12 08_PM" src="https://user-images.githubusercontent.com/56074469/165583325-57af7bce-5ce5-4db2-b3a1-9aabb1d8db7e.png">

- Right above the search bar, there is a carousel showing the recommendations based on the songs which were shown above. The image of the carousel is attached above.

    ![add](https://user-images.githubusercontent.com/56074469/165583338-4ec278d3-64b0-4a5b-b6dc-ce0c9605cbe5.png)

- In case you feel you want to add a song which is not there in our library, there is option which allows you to do that. The image of this attached above. Here you can add the title, artist of the song and then upload the mp3 file. After you upload the song and like it, then the recommendation takes this song into account and then shows various suggestions based on this and the other liked songs.

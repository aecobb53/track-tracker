# TODO / Roadmap

## MVP-2

Trying to get to a useful level.

### Primary

- [X] Data Pages
    - [X] Athletes
        - [X] Find Athlete
        - [X] Display Athlete
    - [X] Teams
        - [X] Find Teams
        - [X] Display Teams
    - [X] Records
- [ ] UI
    - [X] All unimplemented pages have Unimplemented responses
    - [X] All pages have a description at the top
    - [ ] All pages have more explanation about how to effectively use them as a dropdown
    - [ ] Better descriptions on fields you can interact with
    - [X] Remove sidebar and only have it on the home page - Probably. Confirm I want this
    - [X] Home page has description/link for each page
- [ ] Backend
    - [X] favicon.ico
    - [X] robots.txt
    - [ ] Auth
- [ ] Data
    - [ ] Fix prod data
    - [ ] Upload the rest of the data

- IMPLEMENTATION THOUGHT - Add a dudner eq and dudner gt... functions to the mark class so you can compare and sort by marks



Thoughts
- [ ] Marks
    - [x] Needs a header to indicate its athlete data
    - [x] needs a left margin
    - [X] Needs a filter secion
    - [X] Needs Gender toggle or dial
    - [X] Submit needs to be larger
    - [X] All/apply needs to be larger
    - [X] Set page limit
    - [X] Pagination
        - For pagination I will need to query the entire table to see what meets the criteria to know how many 
        pages could exist
        - I also need to change the responses back to a key: value of lists so I can add other keys like pagination
        info
    - [X] All/Apply needs to be on different lines
    - [X] No results found
    - [X] Rename Submit to Request
    - [X] Move Requst button lower
    - [X] Remove add_style for style items


- [ ] Athlete
    - [X] Needs a header to indicate its athlete data
    - [X] needs a left margin
    - [X] Needs Gender toggle or dial
    - [X] Submit needs to be larger
    - [X] All/apply needs to be larger
    - [X] Set page limit
    - [X] Pagination
    - [X] All/Apply needs to be on different lines
    - [X] No results found
    - [X] Rename Submit to Request
    - [X] Move Requst button lower
    - [X] Remove add_style for style items
    - [X] Dont forget about athlete specific page

- [ ] Team
    - [X] Needs a header to indicate its athlete data
    - [X] needs a left margin
    - [ ] ~Needs Gender toggle or dial~
    - [X] Submit needs to be larger
    - [X] All/apply needs to be larger
    - [X] Set page limit
    - [X] Pagination
    - [X] All/Apply needs to be on different lines
    - [X] No results found
    - [X] Rename Submit to Request
    - [X] Move Requst button lower
    - [X] Remove add_style for style items
    - [X] Dont forget about team specific page

- [X] Athlete specific page
    - [X] Add records based on mark values
    - [X] I believe this means I need to implement records and mark comparison

- [X] record needs an unimplemented response
- [X] resources needs an unimplemented response
- [ ] Sort by Meet doesnt seem to be working
- [ ] Verify other sorts are working
- [ ] Before data load, fix all event headers to a uniform format
- [ ] DIn disciption mention 
- [ ] Home page move add_style to add_class and styles at the bottom
- [ ] Set page title as a link to home page
- [ ] Home page needs a left margin for headers


### Stretch

- [ ] Data Pages
    - [ ] Development Roadmap posted
    - [ ] Health of service page or endpoint from UI?
    - [ ] Request data, functionality, bug fix
- [ ] UI
    - [ ] A way to request data or functionality
- [ ] Backend
    - [ ] /about
    - [ ] /service-info
- [ ] Data
    - [ ] Add weather data for each meet location
    - [ ] Two meets arent loading. Fix

### Bug
- [ ] Athletes name got dropped from display. I suspect the parent isnt being grabbed which is reasonable.
    - This could actually be a neat safety feature. If you dont have permissions you see results just not names
- [ ] Drop the #A from the start of events if they are at a state track meet?
    - Rename all events to what I would expect of Mens/Womens ...

## Roadmap

- [ ] Data Pages
    - [ ] Events
    - [ ] Resources - FHS Team links
    - [ ] About
    - [ ] Contact Author
    - [ ] video Download Links?
    - [ ] Schedule - Meet schedule for this or previous years
- [ ] UI
    - [ ] Description on every field
    - [ ] Add a data sort order capability
    - [ ] Pagination
    - [ ] Data line count
    - [ ] Boarder around table to make it look nicer
    - [ ] Light and dark modes
    - [ ] Verify readable in different light levels
    - [ ] Verify useful at different screen sizes
    - [ ] Move Side bar to the top for now
    - [ ] Long term find a way to work side bar back in if I can
    - [ ] Men/Women toggle or dropdown
    - [ ] Typo `Plate` - `Place`
    - [ ] Wind needs Units
    - [ ] When no results found, inform the user
    - [ ] In filtering allow a '=' list such as Heat=1,2
    - [ ] Button on results to indicate bad data and request or implement an update
    - [ ] Change scaling based on screen size. Computer or phone?
    - [ ] Change default columns based on computer or phone
    - [ ] Mark data as bad or update data on the spot
    - [ ] Move `add_style` to style docs for more global application
    - [ ] On the team and probably also athlete pages add a way to select which years to show
        - [ ] By default age off old athletes from the team page
        - [ ] While im at it, age off old results from all pages except athlete specific pages at least by default
- [ ] Backend
    - [ ] Parse response to determine rest, computer, or phone
- [ ] Data
    - [ ] Auto Scrapping with opening a window on the system to pull html?
- [ ] Generic endpoints to consider
TrackTracker  | INFO:     172.23.0.1:56842 - "GET /favicon.ico HTTP/1.1" 404 Not Found
TrackTracker  | INFO:     172.23.0.1:56842 - "GET /ads.txt HTTP/1.1" 404 Not Found
TrackTracker  | INFO:     172.23.0.1:40570 - "GET /js/twint_ch.js HTTP/1.1" 404 Not Found
TrackTracker  | INFO:     172.23.0.1:53906 - "GET /.env HTTP/1.1" 404 Not Found

## MVP-1

Get enough pulled together to deploy on server.

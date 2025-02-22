# TODO / Roadmap

## MVP-2

Trying to get to a useful level.

### Primary

- [ ] Data Pages
    - [ ] Athletes
        - [ ] Find Athlete
        - [ ] Display Athlete
    - [ ] Teams
        - [ ] Find Teams
        - [ ] Display Teams
    - [ ] Records
    - [ ] Schedule - Meet schedule for this or previous years
- [ ] UI
    - [ ] All unimplemented pages have Unimplemented responses
    - [ ] All pages have a description at the top
    - [ ] All pages have more explanation about how to effectively use them as a dropdown
    - [X] Remove sidebar and only have it on the home page - Probably. Confirm I want this
    - [X] Home page has description/link for each page
- [ ] Backend
    - [ ] favicon.ico
    - [ ] robots.txt
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
    - [ ] ~~Trigger columsn on check??~~
    - [X] Set page limit
    - [ ] Pagination
        - For pagination I will need to query the entire table to see what meets the criteria to know how many 
        pages could exist
        - I also need to change the responses back to a key: value of lists so I can add other keys like pagination
        info
    - [X] All/Apply needs to be on different lines
    - [X] No results found
    - [X] Rename Submit to Request
    - [X] Move Requst button lower


- [ ] Athlete
    - [ ] Needs a header to indicate its athlete data
    - [ ] needs a left margin
    - [ ] Needs Gender toggle or dial
    - [ ] Submit needs to be larger
    - [ ] All/apply needs to be larger
    - [ ] Trigger columsn on check??
    - [ ] Set page limit
    - [ ] Pagination
    - [ ] All/Apply needs to be on different lines
    - [ ] No results found
    - [ ] Rename Submit to Request
    - [ ] Move Requst button lower

- [ ] Team
    - [ ] Needs a header to indicate its athlete data
    - [ ] needs a left margin
    - [ ] Needs Gender toggle or dial
    - [ ] Submit needs to be larger
    - [ ] All/apply needs to be larger
    - [ ] Trigger columsn on check??
    - [ ] Set page limit
    - [ ] Pagination
    - [ ] All/Apply needs to be on different lines
    - [ ] No results found
    - [ ] Rename Submit to Request
    - [ ] Move Requst button lower

- [X] record needs an unimplemented response
- [X] resources needs an unimplemented response
- [ ] Sort by Meet doesnt seem to be working
- [ ] Verify other sorts are working

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
- [ ] Backend
    - [ ] Parse response to determine rest, computer, or phone
- [ ] Data
    - [ ] Auto Scrapping with opening a window on the system to pull html?

## MVP-1

Get enough pulled together to deploy on server.

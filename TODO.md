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

- IMPLEMENTATION THOUGHT - Add a dudner eq and dudner gt... functions to the result class so you can compare and sort by results



Thoughts
- [ ] Results
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
    - [X] Add records based on result values
    - [X] I believe this means I need to implement records and result comparison

- [X] record needs an unimplemented response
- [X] resources needs an unimplemented response
- [ ] Sort by Meet doesnt seem to be working
- [ ] Verify other sorts are working
- [ ] Before data load, fix all event headers to a uniform format
- [ ] DIn disciption mention 
- [ ] Home page move add_style to add_class and styles at the bottom
- [ ] Set page title as a link to home page
- [ ] Home page needs a left margin for headers
- [ ] Records page takes a while to load or struggles to load
- [X] Add Team to records page
- [X] Add graduation year to team and records pages
- [ ] Pull historic records for state and FHS
- [X] Async any endpoint
- [ ] Verify it works on mobile


# High importance
- [X] Verify it works on mobile
- [X] Date to American bullshit
- [ ] Find a better final row for tables that display the records for the event
- [X] Move filters into Query section and move Request next to Apply for ease of readability. Maybe then change Apply to "Update Columns"
- [ ] Better table color schema
- [X] Fix data loader where relays still arent fixing the event name

# Easy to implement
- [X] Remove I from descriptions.
- [X] Remove "query" from everywhere
- [X] "sort item 1" to "sort column 1"
- [X] Switch the firstname/lastname columns in athlete view since they are default sorted by last

# Important
- [X] Searching for meets or athletes need to accept case insensitive or maybe even wildcards
- [ ] larger fonts for mobile
- [X] Fix the About
- [ ] Teams only show teams with over 25 results but allow for getting all

# Mobile
- [X] Pagination needs to be larger in general to be able to click easier
- [X] Banner needs to be larger
- [ ] Unset form filling out as its stealing focus on a phone
- [X] Make .big-button 's larger
- [X] Banner is good, maybe a bit large. Need to allow the home and about to go above the words. Maybe put them in first?
- [ ] Link colors clash with green as they are blue on green



- [ ] Default all Teams to fairview
- [ ] Default date to this year
event is time first and a different results first
filter by current students and look at their previous years



- [x] Fix color from dark to FHS.
    - [ ] Maybe even a light/dark mode
- [ ] Remove I from descriptions.
    - [ ] Maybe even do away with descriptions
- [ ] Remove "query" from everywhere
- [ ] Try to mentally search for use cases and see if its effective at providing data
- [ ] Dropdowns for
    - [ ] events
    - [ ] teams
    - [ ] meets
    - [ ] Could have a '+' to add multiple OR operations
- [ ] Verify it works on mobile
- [X] Remove operators like "<=" for words like "Less than or equal to"
- [x] Date to American bullshit
    - [x] Backend
    - [x] UI
- [ ] Find a better final row for tables that display the records for the event
    - [ ] This could even entail only showing this or not at all but allow users to filter by result value and thus the last row would be the current record
- [X] link needs to be the whole tile not just text on main page
- [ ] Move filters into Query section and move Request next to Apply for ease of readability. Maybe then change Apply to "Update Columns"
- [ ] Units on wind
- [ ] Add different ways to query, filter, and display results on Team and Athlete pages
    - [ ] Maybe include hidden elements that can be toggled like the tables are
    - [ ] Another idea is send a larger payload with lots of hidden data and you can select the display style. As long as the paylaods dont get too large
- [ ] Searching for meets or athletes need to accept case insensitive or maybe even wildcards
    - [ ] add search fields for names and teams that store all lowercase but only return the uppercase versions
- [ ] For records save in memory the current everything and update periodicly
- [ ] Add an endpoint to return the enums for Teams and Events
    - [ ] This would need to be updated every so often on the backend
- [ ] Better table color schema
- [ ] May need to look into a way to pull to populate a page if it starts to take too long
- [X] Home and about links need to be buttons and larger
- [ ] separate results from record
- [ ] Teams page add counts for each grade?
- [ ] Teams only show teams with over 25 results but allow for getting all
- [ ] larger fonts for mobile
- [ ] For teams allow a user to order by Athlete Name, Graduation Year, Event, Meet, Gender
- [ ] Maybe have the background of the table more muted and allow different meets to have different colors
- [ ] Maybe sort by result or date
- [ ] For athletes allow a user to order by Meet, Event. Then sort by Result speed or date
- [X] Move results away from primary spot and drop the star. This should be very powerful but not the first page people should go to. Add a FHS team page direct link
- [ ] Low data mode where minimal data is transfered. Maybe put the botton in the center of the header. "Low wifi mode"?
- [ ] Put a Freshman, Sophomore, Junior, Senior indicator next to grad years?
- [ ] "sort item 1" to "sort column 1"
- [ ] Find a way to pursist the database
- [ ] Look into having multiple heads running and what that will help with
- [ ] "First Name", "Last Name", and "Graduation Year" not toggling correctly on athlete page
- [ ] "Athlete Count" not a toggle on Team page


Concepts:
- [ ] I want to see my personal best performance
- [ ] I want to see how I improved throughout the year
- [ ] I want to see which of my athletes is the best
- [ ] I want to see how each athlete has been improving
- [ ] I want to see how I or an athlete performed at all of their events on this meet
- [ ] I want to see how each of my athletes performed at this meet



Notes

Hard to read too dark
background could use color or pictures
Remove I from all descriptions
Move query to search
Double check results are an effective way to explain things
	Maybe Results
Dropdown for events?
Ranges should be 'up to' 'equal to' instead of <=, =
Date to American bullshit
Dashes are kinda weird in the tables
Filter sorted
Units on Wind
Meet lines could use different color hues for each meet or different data
	OR different meets between each set of data
Dropdown for events should have an "add button"
Meet names need to accept non capital convention

Concept: I want to see my best performers in a particular event

For school or athlete filtering, save the raw and a lowercase version so you can filter on lowercase anything. 
For records load the page and then sequentially get results for each event
    This would also require an endpoint for all current events
    This could also be taken care of as a background process. Something like every 10 minutes 
        go through every result and store teams, events, and records in memory
        or create a "current records" table but I dont like this idea
    Idea. Every day medium speed go through every record and update the list of all events that is stored in memory. Then every 10 minutes go event by event to see if there are any updates. This could also be configured to only be every hour during the week but every 10 minutes on the weekends. 
        This would be just so events could be added during a meet but if this isnt happening this really isnt required
Find a better table color schema
Find a better record color schema
Maybe add a way to incrementally add results on things like the teams pages even so they load slightly faster
For teams allow a user to order by Athlete Name, Graduation Year, Event, Meet
Maybe have the background of the table more muted and allow different meets to have different colors
Maybe sort by result or date
For athletes allow a user to order by Meet, Event. Then sort by Result speed or date
Move results away from primary spot and drop the star. This should be very powerful but not the first page people should go to. Add a FHS team page direct link

Center Primary Page
Fairview Colors?
Color Code lines by gendeR?
Table columns after Request is confusing
Change All to Select All or something
After Registered clicked change color or indicate it was clicked?
Click to hilight a row in the table?
pull up athletes by graduation year
"sort item 1" to "sort column 1"


Put a Freshman, Sophomore, Junior, Senior indicator next to grad years?







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
    - [ ] Result data as bad or update data on the spot
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

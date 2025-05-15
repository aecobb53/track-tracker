# TODO / Roadmap

## Version 1.3
- [ ] Data Pages
- [ ] Hidden or Dev pages
    - [ ] Dev dashboard `/dev/`?
    - [ ] Health of service page or endpoint from UI?
    - [ ] Recruiter
- [ ] UI
    - [ ] A way to notify data is wrong (in line with data)?
    - [ ] When no results found, inform the user
    - [ ] On the team and probably also athlete pages add a way to select which years to show
        - [ ] By default age off old athletes from the team page
        - [ ] While im at it, age off old results from all pages except athlete specific pages at least by default
    - [ ] Explore dropdowns to see if its tenable 
    - [ ] Verify sorting is working
    - [ ] Verify margins are set and look nice
- [ ] Backend
    - [ ] /service-info
    - [ ] Persist some data like different events, teams etc.
        - [ ] Return data from an endpoint
    - [ ] Only return data for active students unless asking for everything
    - [ ] Generally clean up the code
- [ ] Data
    - [ ] Pull historic records for state and FHS
    - [ ] Upload the rest of the data
    - [ ] Two meets arent loading. Fix
- [ ] Mobile
    - [ ] Verify readable in different light levels
    - [ ] Verify useful at different screen sizes


## Roadmap

- [ ] Data Pages
    - [ ] Request data, functionality, bug fix
    - [ ] Development Roadmap posted
    - [ ] Records
    - [ ] PR's page. Maybe driven by a date or a meet or just all PRs for each meet or something like that
- [ ] Hidden or Dev pages
    - [ ] Health of service page or endpoint from UI?
    - [ ] Recruiter
- [ ] UI
    - [ ] A way to request data or functionality (in line with data)?
    - [ ] Description on every field
    - [ ] Verify readable in different light levels
    - [ ] Verify useful at different screen sizes
    - [ ] When no results found, inform the user
    - [ ] Button on results to indicate bad data and request or implement an update
    - [ ] Change scaling based on screen size. Computer or phone?
    - [ ] Change default columns based on computer or phone
    - [ ] On the team and probably also athlete pages add a way to select which years to show
        - [ ] By default age off old athletes from the team page
        - [ ] While im at it, age off old results from all pages except athlete specific pages at least by default
    - [ ] Light and dark modes
    - [ ] Dropdowns for
        - [ ] events
        - [ ] teams
        - [ ] meets
        - [ ] Could have a '+' to add multiple OR operations
    - [ ] Verify sorting is working
    - [ ] Verify margins are set and look nice
    - [ ] add the ability to hide/unhide sections of very large documents 
        - like meets or events when they get long
        - like different events or meets so you can compare similar ones more easilly
    - [ ] Results page needs to include class sorting and column
    - [ ] Light/Dark mode?
    - [ ] Teams Find page add counts for each grade, gender?
    - [ ] Teams find page add district
    - [ ] "MSAthlete Count" not a toggle on Team page
    - [ ] For teams allow a user to order by MSAthlete Name, Graduation Year, Event, Meet, Gender, Varsity/JV?
        - [ ] Add to Season Selector Gender
        - [ ] Add to Season Selector and Class?
        - [ ] Is there a way to select JV/Varsity just Varsity or just JV?
    - [ ] For athletes allow a user to order by Meet, Event. Then sort by Result speed or date
    - [ ] Low data mode where minimal data is transfered. Maybe put the botton in the center of the header. "Low wifi mode"?
    - [ ] "First Name", "Last Name", and "Graduation Year" not toggling correctly on athlete page
        - [ ] Look into all toggles and query arguments to ensure they are working
- [ ] Backend
    - [ ] Auth
    - [ ] Parse response to determine rest, computer, or phone
    - [ ] /service-info
    - [ ] Persist some data like different events, teams etc.
        - [ ] Return data from an endpoint
    - [ ] Only return data for active students unless asking for everything
        - Use the current year variable to determine if graduating in 0-4 years?
    - [ ] Fix endpoint function names
    - [ ] Fix imports as they are sometimes not being added to init and whatnot
    - [ ] Generally clean up the code
    - [ ] Create GitHub actions and a CICD pipeline
    - [ ] Look into auto deploys on the server?
        - [ ] This could be a cool "if version updates and tests pass -> deploy" scenario
    - [ ] Low data mode where minimal data is transfered. Maybe put the botton in the center of the header. "Low wifi mode"?
- [ ] Data
    - [ ] Pull historic records for state and FHS
    - [ ] Upload the rest of the data
    - [ ] Auto Scrapping with opening a window on the system to pull html?
    - [ ] Add weather data for each meet location
    - [ ] Two meets arent loading. Fix
    - [ ] Find a way to pursist the database
    - [ ] Look into having multiple heads running and what that will help with
    - [ ] Gather which district each team is from?
- [ ] Mobile
    - [ ] Determine if font is large enough
    - [ ] Determine if colors look good in sun and shade
    - [ ] Determine if data load is still good when wifi is low?
    - [ ] Unset form filling out as its stealing focus on a phone


## Bugs



# Use Cases
- I want to see my personal best performance
- I want to see how I improved throughout the year
- I want to see which of my athletes is the best
- I want to see how each athlete has been improving
- I want to see how I or an athlete performed at all of their events on this meet
- I want to see how each of my athletes performed at this meet
- I want to see my best performers in a particular event


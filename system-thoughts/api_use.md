_(fyi: for internal team discussion, not consensus opinion, etc)_

# Using Primefaces components vs. API/JSON/Template

This document attempts to examine factors when examining the decision whether or not to use a Primefaces component.  

  - **Question**: Is your component working for you or are you working for your component?

Below are two rules of thumb which may be applied when adding new UI functionality.

## 1. Use a Primefaces component when:

1. Component matches design or can be tweaked via css, built-in styles
1. Component is performant

## 2. Avoid component when:

1. Changing component design becomes main task.
1. Making component performant adds high overhead/complexity


**Summary for Rules of Thumb**: Do what makes sense in the situation rather than forcing code and design to conform to a component.

---

# Comparison of API/JSON/Template vs. Primefaces Component

This list compares the use of Primefaces components versus using an approach of businss logic/APIs which return JSON and are then coupled with templates (w/o business logic) or javascript components.

For a more in-depth discussion, short and long-term views should be applied, weighing:
  - How will the chosen approach help us accomplish tasks now?  
  - How will the chosen approach effect the project in 1, 2, 5 years?

|#|Capability/Process|API/JSON/Template (server or browser based)|Primefaces Component|Note|
---|:---:|:---:|:---:|---
|1|**Development Time**|**Medium**|**High**\*|\*When component doesn't fit task.|
|2|**Automated Testing** (Rest Assured)|**Yes**|**No**|
|3|**HTML Customization**|**Easy/Medium**\*|**Difficult**\*\*|\*Many tools available or raw HTML (Java templating, jquery, datatables, angular, react, etc, etc)  \*\*Design limited to Primeface components. (ref: dataset page file listing)|
|4|**Troubleshooting**: Business Logic/Design Separate|**Yes**\*|**No**|\*Easier to identify issues, especially with automated testing of business logic.  Right away "50% easier" -- easily determine whether issue is in business logic or template|
|5|**Performance Tuning**|**More choices**/Business logic not in component|**Often constrained** by component||
|6|**Code reuse**|**High**\*|**Low/Medium**\*\*|\*API endpoints/templates can be re-used. \*\*Components tightly tied to Business Logic|
|7|Javascript Dependent|**Yes** - if browser based|**Yes**|
|8|508 Compliance with Forms|**It depends**|**No**|
|9|**Widely used in open source community**|**Yes**\*|**No** \*\*|\*More community -> Great pool of potential contributors, stackoverflow, etc) \*\*In 2016 we were believed to be only open source project|
|10|Widely used paradigm|**Yes**|**No**\*|\*Industry shift to microservices, other frameworks, Oracle pulling resources, fewer programmers in their 20s, etc.|
|11|Selenium Automated Testing|**Yes**|**No**\*|\*Requires significant programming (time prohibitive)|



# Consistency

There is something to be said for using Primefaces components because they are consistent with other parts of the system.  __However__, that view should be factored in with the points in the chart above and, more importantly, with a longer term strategic view of the system if the goals include:
  - Having more API endpoints
  - Increasing the number of code contributors
  - Improving automated testing
  - Shifting some parts of the system to separate microservices to improve scalability

- click to enlarge: <a href="https://github.com/IQSS/dataverse-helper-scripts/blob/master/system-thoughts/api-diagram-01.png?raw=true"><img src="https://github.com/IQSS/dataverse-helper-scripts/blob/master/system-thoughts/api-diagram-01.png?raw=true" width="450" /></a>

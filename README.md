# Chamber of Commerce email crawler

This project is for crawling the sites of Chambers of Commerce to get contact info (emails and phone #'s) from all the businesses. It will completely crawl through each of the sites found on the Chamber of Commerce page, and look for contact info in the form of `tel:` or `mailto:` links in the HTML. Once it gets all of the addresses, it will sort by likeliness of being the main contact.

Finally, it will be compared to a pre-existing list of businesses that have already been contacted.

## Steps

Currently works specifically for Andersonville Chamber of Commerce in Chicago, IL. Gets the [main page](http://business.andersonville.org/list), then crawls the categories on the page to get sub pages i.e. [culture and entertainment](http://business.andersonville.org/list/ql/culture-entertainment-recreation-27), then finally a link to a [specific business](http://business.andersonville.org/list/member/chicago-tap-theatre-1208) which leads to their own website and domain. This is crawled until we have all the domains of all the businesses.

Once business sites are stored, we crawl each of them to look for contact info like phone number and email. This will take a while. All are stored in a JSON file but emails are then further processed to get the most ideal email.

## Running

This is best run using docker and docker-compose. You can build and run the full thing using `docker-compose up --build`. Or you can do it in parts by running each service with `docker-compose -f docker-compose.dev.yaml up <SERVICE> --build`.

Not currently in docker but you can also 

## TODO
- Add logging
- Add testing
- Error handling in case Chamber of Commerce website change
- Make more configurable to other Chamber of Commerce sites
- Run coc_crawler and biz_crawler in parallel

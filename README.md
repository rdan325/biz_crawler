# Chamber of Commerce email crawler

This project is for crawling the sites of Chambers of Commerce to get contact info (emails and phone #'s) from all the businesses. It will completely crawl through each of the sites found on the Chamber of Commerce page, and look for contact info in the form of `tel:` or `mailto:` links in the HTML. Once it gets all of the addresses, it will sort by likeliness of being the main contact.

Finally, it will be compared to a pre-existing list of businesses that have already been contacted.

### Steps

1. Get links of homepage URL
2. Find all businesses websites
3. Crawl sites completely
4. Find `tel:` and `mailto:` links
5. Save links to a file (json, csv?)
6. Match to existing file

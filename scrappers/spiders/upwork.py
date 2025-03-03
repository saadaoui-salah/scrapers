import scrapy
import json


class Profile(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    hourly_rate = scrapy.Field()
    title = scrapy.Field()
    skills = scrapy.Field()
    success_score = scrapy.Field()
    earning = scrapy.Field()
    reviews = scrapy.Field()
    education = scrapy.Field()
    verified = scrapy.Field()
    english_proficiency = scrapy.Field()
    certifications = scrapy.Field()
    keywords = scrapy.Field()

class UpworkSpider(scrapy.Spider):
    name = "upwork"
    start_urls = ["https://www.upwork.com/api/graphql/v1?alias=visitorFreelancerSearchV2"]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.upwork.com/nx/search/talent/?loc=pakistan&pt=independent&page=3",
        "X-Upwork-Accept-Language": "en-US",
        "Vnd-Eo-Visitorid": "154.249.190.27.1740674940570000",
        "Content-Type": "application/json",
        "Vnd-Eo-Trace-Id": "9189aa698a80ba95-ALG",
        "Vnd-Eo-Span-Id": "b4b71fc6-3286-4b94-970c-0fa3e08c4ffe",
        "Vnd-Eo-Parent-Span-Id": "62c9836c-298a-4600-a97c-14d60bbbd2f7",
        "Authorization": "Bearer oauth2v2_4e18e917f314fda9106947a555b6be2c",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers"
    }

    def make_payload(self, page):
        data = {
            "query": """
            query VisitorFreelancerSearch($request: VisitorFreelancerSearchV2Request!) {
                search {
                    universalSearchNuxt {
                        visitorFreelancerSearchV2(request: $request) {
                            pagingInfo {
                                total
                                offset
                                count
                                originTotal
                                pagesTotal
                                page
                            }
                            adaptiveSkills {
                                id
                                prefLabel
                                ontologyId
                            }
                            relevantSkillIds
                            resultFlags {
                                portfolioSearch
                            }
                            facets {
                                hourlyRate {
                                    key
                                    value
                                }
                            }
                            profiles {
                                individualTotalEarnings
                                agencyTotalEarnings
                                offerConsultations
                                jobSummariesAssignmentRids
                                personId
                                profileId
                                totalCompletedJobs
                                rankInfo {
                                    d
                                    iv
                                }
                                vetted
                                profile {
                                    identity {
                                        id
                                        ciphertext
                                    }
                                    personAvailability {
                                        purchasedInvitationBadge {
                                            active
                                        }
                                    }
                                    personalData {
                                        title
                                        firstName
                                        lastName
                                        description
                                        location {
                                            country
                                            state
                                            city
                                            region
                                            subregion
                                            timezone
                                            zip
                                        }
                                        chargeRate {
                                            rawValue
                                            currency
                                        }
                                        portrait {
                                            portrait100
                                        }
                                        profileUrl
                                    }
                                    skills {
                                        ontologySkill {
                                            id
                                            preferredLabel
                                            prettyName
                                            definition
                                        }
                                    }
                                    projectList {
                                        totalProjects
                                        projects {
                                            id
                                            title
                                            projectUrl
                                            thumbnail
                                            category
                                            categoryId
                                            subCategory
                                            description
                                            videoUrl
                                            public
                                        }
                                    }
                                    verifications {
                                        idBadgeStatus
                                        idVerified
                                    }
                                    agencies {
                                        defaultAgencyId
                                        agencies {
                                            orgId
                                            ciphertext
                                            name
                                            classifications {
                                                id
                                                name
                                            }
                                            logo
                                        }
                                    }
                                    preferences {
                                        hideEarnings
                                        hideJss
                                    }
                                    profileAggregates {
                                        nSS100BwScore
                                        topRatedStatus
                                        topRatedPlusStatus
                                        totalHours
                                        totalHourlyJobs
                                        totalEarnings
                                        totalFixedJobs
                                    }
                                    communityCertificates {
                                        expirationDate
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
            "variables": {
                "request": {
                    "individualEarningsSearch": True,
                    "paging": {"start": page*50, "rows": 50},
                    "visitorId": "154.249.190.27.1740674940570000",
                    "facets": ["hourly_rate"],
                    "addGoodSummaries10Rids": True,
                    "countries": ["Pakistan"],
                    "providerType": "Independent",
                    "agencySearch": False
                }
            }
        }
        return json.dumps(data)

    def start_requests(self):
        for i in range(11):
            yield scrapy.Request(
                url=self.start_urls[0],
                method="POST",
                headers=self.headers,
                body=self.make_payload(i),
                callback=self.parse,
            )

    def parse(self, response):
        data = response.json()['data']['search']['universalSearchNuxt']['visitorFreelancerSearchV2']
        headers = {
            "Host": "www.upwork.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.upwork.com/nx/search/talent/details/~01b208d331946ec1d2/profile?loc=pakistan&pt=independent&page=3&pageTitle=Profile&_modalInfo=%5B%7B%22navType%22%3A%22slider%22,%22title%22%3A%22Profile%22,%22modalId%22%3A%221740676234846%22%7D%5D",
            "X-Odesk-User-Agent": "oDesk LM",
            "X-Requested-With": "XMLHttpRequest",
            "X-Upwork-Accept-Language": "en-US",
            "Vnd-Eo-Trace-Id": "9189aa698a80ba95-ALG",
            "Vnd-Eo-Span-Id": "5ee4b171-ff2c-442c-bf6b-d818a06e8151",
            "Vnd-Eo-Parent-Span-Id": "62c9836c-298a-4600-a97c-14d60bbbd2f7",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Te": "trailers"
        }
        for profile in data['profiles']:
            url = "https://www.upwork.com/freelancers/public/api/v1/freelancer/profile/{}/details?excludeAssignments=true"
            item = Porfile()
            item['verified'] =  True if profile['verifications']['idBadgeStatus'] == 'PASSED' else False
            item['earning'] = profile['profileAggregates']['totalEarnings']
            item['success_score'] = profile['profileAggregates']['nSS100BwScore']
            yield scrapy.Request(
                url=url.format(profile['profile']['identity']['ciphertext']),
                headers=self.headers,
                callback=self.parse_profile,
                meta={'item': item}
            )

    def parse_profile(self, response):
        data = response.json()['profile']
        lang = next(filter(lambda x: x['language']['iso639Code'] == 'en', data['languages']), {'proficiencyLevel':{'proficiencyTitle':None}})
        profile = data['profile']
        item['name'] = profile['name']
        item['country'] = profile['location']['country']
        item['city'] = profile['location']['city']
        item['hourly_rate'] = f"{profile['hourlyRate']['amount']} {profile['hourlyRate']['currencyCode']}"
        item['title'] = profile['title']
        item['skills'] = [skill['prettyName'] for skill in profile['skills']]
        item['education'] = [edu['institutionName'] for edu in data['education']]
        item['reviews'] = profile['stats']['rating']
        item['english_proficiency'] = lang['proficiencyLevel']['proficiencyTitle']
        item['certifications'] = [cert['certificate']['name'] for cert in profile['certificates']]
        yield item

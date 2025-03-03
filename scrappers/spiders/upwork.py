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
    profile_link = scrapy.Field()

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
        "Vnd-Eo-Trace-Id": "91a6150609692826-ALG",
        "Vnd-Eo-Span-Id": "9797e157-9928-4c06-83f8-a91c2b7976ef",
        "Vnd-Eo-Parent-Span-Id": "020138c7-3533-42ee-b2a7-5b30251c5537",
        "Authorization": "Bearer oauth2v2_a2d750250e02643acfade6351931761b",
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
        for i in range(202):
            yield scrapy.Request(
                url=self.start_urls[0],
                method="POST",
                headers=self.headers,
                body=self.make_payload(i),
                callback=self.parse,
            )

    def parse(self, response):
        data = response.json()['data']['search']['universalSearchNuxt']['visitorFreelancerSearchV2']
        for profile in data['profiles']:
            url = "https://www.upwork.com/freelancers/public/api/v1/freelancer/profile/{}/details?excludeAssignments=true"
            item = Profile()
            item['verified'] =  True if profile['profile']['verifications']['idBadgeStatus'] == 'PASSED' else False
            item['earning'] = profile['profile']['profileAggregates']['totalEarnings']
            item['success_score'] = profile['profile']['profileAggregates']['nSS100BwScore']
            item['profile_link'] = profile['profile']['personalData']['profileUrl']
            yield scrapy.Request(
                url=url.format(profile['profile']['identity']['ciphertext']),
                headers=self.headers,
                callback=self.parse_profile,
                meta={'item': item}
            )

    def parse_profile(self, response):
        data = response.json()['profile']
        item = response.meta['item']
        stats = data['stats']
        lang = None
        if data['languages']:
            lang = next(filter(lambda x: x['language']['iso639Code'] == 'en', data['languages']), {'proficiencyLevel':{'proficiencyTitle':None}})
            lang = lang['proficiencyLevel']['proficiencyTitle']
        profile = data['profile']
        item['name'] = profile['name']
        item['country'] = profile['location']['country']
        item['city'] = profile['location']['city']
        item['hourly_rate'] = f"{stats['hourlyRate']['amount']} {stats['hourlyRate']['currencyCode']}"
        item['title'] = profile['title']
        item['skills'] = [skill['prettyName'] for skill in profile['skills']]
        if data['education']:
            item['education'] = [edu['institutionName'] for edu in data['education']]
        item['reviews'] = data['stats']['rating']
        item['english_proficiency'] = lang
        if data['certificates']:
            item['certifications'] = [cert['certificate']['name'] for cert in data['certificates']]
        yield item

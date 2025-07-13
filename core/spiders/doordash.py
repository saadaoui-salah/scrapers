import scrapy
import json
import base64 
import os

class DoordashSpider(scrapy.Spider):
    name = "doordash"
    api_key = os.getenv('ZYTE_API')
    auth_str = f"{api_key}:".encode()
    auth_header = base64.b64encode(auth_str).decode()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_header}',
    }
    query = "query categorySearch($storeId: ID!, $categoryId: ID!, $subCategoryId: ID, $limit: Int, $cursor: String, $filterKeysList: [String!], $sortBysList: [RetailSortByOption!]!, $filterQuery: String, $aggregateStoreIds: [String!]) {\n  retailStoreCategoryFeed(\n    storeId: $storeId\n    l1CategoryId: $categoryId\n    l2CategoryId: $subCategoryId\n    limit: $limit\n    cursor: $cursor\n    filterKeysList: $filterKeysList\n    sortBysList: $sortBysList\n    filterQuery: $filterQuery\n    aggregateStoreIds: $aggregateStoreIds\n  ) {\n    ...RetailCategoryFeedFragment\n    filtersList {\n      ...RetailFilterFragment\n      __typename\n    }\n    pillFilters {\n      ...RetailPillFilterFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RetailCategoryFeedFragment on RetailCategoryFeed {\n  id\n  categoryId\n  urlSlug\n  name\n  storeId\n  imageUrl\n  storeId\n  totalItemCount\n  l2Categories {\n    ...RetailL2CategoryFragment\n    __typename\n  }\n  selectedL2Category {\n    ...RetailL2CategoryFragment\n    __typename\n  }\n  products {\n    ...RetailItemDetailsFragment\n    __typename\n  }\n  pageInfo {\n    ...PageInfoFragment\n    __typename\n  }\n  sortOptions {\n    name\n    sortBy\n    __typename\n  }\n  groups {\n    id\n    name\n    __typename\n  }\n  legoSectionBodyList {\n    ...FacetV2Fragment\n    __typename\n  }\n  legoRetailItems {\n    ...FacetV2Fragment\n    __typename\n  }\n  __typename\n}\n\nfragment RetailL2CategoryFragment on RetailL2Category {\n  id\n  subCategoryId\n  urlSlug\n  name\n  storeId\n  imageUrl\n  __typename\n}\n\nfragment RetailItemDetailsFragment on RetailItem {\n  ...BaseRetailItemDetailsFragment\n  productVariants {\n    ...BaseRetailItemDetailsFragment\n    __typename\n  }\n  similarProducts {\n    ...BaseRetailItemDetailsFragment\n    __typename\n  }\n  __typename\n}\n\nfragment BaseRetailItemDetailsFragment on RetailItem {\n  id\n  urlSlug\n  name\n  description\n  storeId\n  menuId\n  imageUrl\n  price {\n    ...MonetaryFieldsFragment\n    __typename\n  }\n  metadata {\n    ...metaDataFragment\n    __typename\n  }\n  variation {\n    variant\n    size\n    swatch {\n      ...RetailItemSwatchFragment\n      __typename\n    }\n    visualVariant {\n      name\n      image\n      type\n      __typename\n    }\n    __typename\n  }\n  shouldHideNutritionalHeaders\n  nutritionalInfo {\n    ...NutritionalInfoFragment\n    __typename\n  }\n  details\n  imageUrlsList\n  soldAsInfoLongText\n  soldAsInfoShortText\n  displayUnit\n  unit\n  purchaseType\n  estimatePricingDescription\n  calloutDisplayString\n  itemMsid\n  ddSic\n  badgeEntries\n  metadataEntries\n  logging\n  badges {\n    ...BadgeFragment\n    __typename\n  }\n  adsMetadata {\n    ...AdsMetadataFragment\n    __typename\n  }\n  priceList {\n    ...PriceFragment\n    __typename\n  }\n  soldAsInfoTextList {\n    ...SoldAsInfoTextFragment\n    __typename\n  }\n  variantInfo {\n    ...VariantInfoFragment\n    __typename\n  }\n  l1Category {\n    ...CategoryInfoFragment\n    __typename\n  }\n  l2Category {\n    ...CategoryInfoFragment\n    __typename\n  }\n  availablePromotion {\n    ...RetailItemPromotionDetailsFragment\n    __typename\n  }\n  quickAddContext {\n    ...QuickAddContextFragment\n    __typename\n  }\n  optionList {\n    ...OptionListFragment\n    __typename\n  }\n  ratings {\n    ...RetailItemRatingFragment\n    __typename\n  }\n  taxLabel\n  __typename\n}\n\nfragment metaDataFragment on ConvenienceProductMetadata {\n  soldAsInfo {\n    measurementUnit\n    measurementFactor {\n      decimalPlaces\n      unitAmount\n      __typename\n    }\n    measurementPrice {\n      currency\n      displayString\n      decimalPlaces\n      unitAmount\n      __typename\n    }\n    __typename\n  }\n  increment {\n    decimalPlaces\n    unitAmount\n    __typename\n  }\n  estimationInfo {\n    approximateSoldAsQuantity {\n      decimalPlaces\n      unitAmount\n      __typename\n    }\n    approximateSoldAsUnit\n    __typename\n  }\n  marketplaceUnit\n  __typename\n}\n\nfragment MonetaryFieldsFragment on AmountMonetaryFields {\n  currency\n  displayString\n  decimalPlaces\n  unitAmount\n  sign\n  symbol\n  __typename\n}\n\nfragment NutritionalInfoFragment on NutritionalMetadata {\n  servingSize\n  servingsPerContainer\n  nutritionAnnotation\n  details {\n    header\n    body\n    __typename\n  }\n  nutrients {\n    label\n    total\n    pctDailyValue\n    subCategories {\n      label\n      total\n      pctDailyValue\n      __typename\n    }\n    __typename\n  }\n  disclaimer\n  __typename\n}\n\nfragment BadgeFragment on Badge {\n  isDashpass\n  type\n  text\n  backgroundColor\n  styleType\n  dlsTagSize\n  dlsTextStyle\n  dlsTagStyle\n  dlsTagType\n  placement\n  leadingIcon\n  leadingIconSize\n  trailingIcon\n  trailingIconSize\n  endTime\n  dlsTextColor\n  brandedDecorator {\n    prefixText\n    postfixText\n    postfixTextLeadingIcon\n    __typename\n  }\n  trailingText {\n    copy\n    dlsTextStyle\n    dlsTextColor\n    __typename\n  }\n  __typename\n}\n\nfragment AdsMetadataFragment on AdsMetadata {\n  campaignId\n  adGroupId\n  auctionId\n  complexDealCampaignId\n  __typename\n}\n\nfragment PriceFragment on RetailPrice {\n  priceType\n  price {\n    ...MonetaryFieldsFragment\n    __typename\n  }\n  additionalDisplayString\n  superscriptedTextGroup {\n    text {\n      text\n      leadingSuperscripts {\n        text\n        scale\n        horizontalOffset\n        verticalOffset\n        __typename\n      }\n      trailingSuperscripts {\n        text\n        scale\n        horizontalOffset\n        verticalOffset\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SoldAsInfoTextFragment on RetailSoldAsInfoText {\n  priceType\n  soldAsInfoShortText\n  soldAsInfoLongText\n  __typename\n}\n\nfragment VariantInfoFragment on VariantInfo {\n  minDiscountedPrice {\n    unitAmount\n    currency\n    displayString\n    __typename\n  }\n  minPrice {\n    unitAmount\n    currency\n    displayString\n    __typename\n  }\n  maxPrice {\n    unitAmount\n    currency\n    displayString\n    __typename\n  }\n  pricePresentationType\n  variantTypeInfo {\n    variantType\n    variantSubTypeInfo {\n      itemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment CategoryInfoFragment on CategoryInfo {\n  name\n  id\n  __typename\n}\n\nfragment RetailItemPromotionDetailsFragment on RetailItemPromotionDetails {\n  promotionTitle\n  termsAndConditions {\n    ...RetailPromotionTermsAndConditionsFragment\n    __typename\n  }\n  promotionDetails\n  __typename\n}\n\nfragment RetailPromotionTermsAndConditionsFragment on RetailPromotionTermsAndConditions {\n  title\n  action\n  copy\n  disclaimer {\n    ...RetailDisclaimerDataFragment\n    __typename\n  }\n  __typename\n}\n\nfragment RetailDisclaimerDataFragment on RetailStoreDisclaimerData {\n  text\n  cms {\n    ...RetailDisclaimerContentFragment\n    __typename\n  }\n  __typename\n}\n\nfragment RetailDisclaimerContentFragment on RetailDisclaimerContent {\n  title\n  description\n  closeAction {\n    ...CloseActionFragment\n    __typename\n  }\n  __typename\n}\n\nfragment CloseActionFragment on CloseAction {\n  label\n  uri\n  __typename\n}\n\nfragment OptionListFragment on OptionList {\n  type\n  id\n  name\n  subtitle\n  selectionNode\n  minNumOptions\n  maxNumOptions\n  minAggregateOptionsQuantity\n  maxAggregateOptionsQuantity\n  minOptionChoiceQuantity\n  maxOptionChoiceQuantity\n  numFreeOptions\n  isOptional\n  storeId\n  titleLayout {\n    actionUrl\n    __typename\n  }\n  options {\n    ...OptionFragment\n    nestedExtrasList {\n      ...NestedExtrasFragment\n      __typename\n    }\n    __typename\n  }\n  validationType\n  flattenedDefaultNodes {\n    __typename\n    ... on DefaultOption {\n      parentId\n      id\n      name\n      nextCursor\n      displayString\n      unitAmount\n      currency\n      decimalPlaces\n      selectedQuantity\n      caloricInfoDisplayString\n      defaultQuantity\n      isRequiredForOptionPromo\n      strikethroughPrice {\n        unitAmount\n        currency\n        displayString\n        symbol\n        decimalPlaces\n        __typename\n      }\n      dietaryTagsList {\n        type\n        abbreviatedTagDisplayString\n        fullTagDisplayString\n        __typename\n      }\n      imgUrl\n      chargeAbove\n      __typename\n    }\n    ... on DefaultOptionList {\n      parentId\n      id\n      name\n      subtitle\n      type\n      selectionNode\n      minNumOptions\n      maxNumOptions\n      minAggregateOptionsQuantity\n      maxAggregateOptionsQuantity\n      minOptionChoiceQuantity\n      maxOptionChoiceQuantity\n      numFreeOptions\n      isOptional\n      options {\n        id\n        name\n        unitAmount\n        currency\n        displayString\n        decimalPlaces\n        nextCursor\n        caloricInfoDisplayString\n        chargeAbove\n        defaultQuantity\n        isRequiredForOptionPromo\n        strikethroughPrice {\n          unitAmount\n          currency\n          displayString\n          symbol\n          decimalPlaces\n          __typename\n        }\n        dietaryTagsList {\n          type\n          abbreviatedTagDisplayString\n          fullTagDisplayString\n          __typename\n        }\n        imgUrl\n        __typename\n      }\n      __typename\n    }\n  }\n  __typename\n}\n\nfragment OptionFragment on FeedOption {\n  id\n  name\n  unitAmount\n  currency\n  displayString\n  decimalPlaces\n  nextCursor\n  caloricInfoDisplayString\n  chargeAbove\n  chargeAboveDisplayString\n  defaultQuantity\n  isRequiredForOptionPromo\n  strikethroughPrice {\n    unitAmount\n    currency\n    displayString\n    symbol\n    decimalPlaces\n    __typename\n  }\n  dietaryTagsList {\n    type\n    abbreviatedTagDisplayString\n    fullTagDisplayString\n    __typename\n  }\n  optionTagsList {\n    type\n    abbreviatedTagDisplayString\n    fullTagDisplayString\n    __typename\n  }\n  minOptionChoiceQuantity\n  maxOptionChoiceQuantity\n  imgUrl\n  __typename\n}\n\nfragment NestedExtrasFragment on OptionList {\n  type\n  id\n  name\n  subtitle\n  selectionNode\n  minNumOptions\n  maxNumOptions\n  minAggregateOptionsQuantity\n  maxAggregateOptionsQuantity\n  minOptionChoiceQuantity\n  maxOptionChoiceQuantity\n  numFreeOptions\n  isOptional\n  storeId\n  titleLayout {\n    actionUrl\n    __typename\n  }\n  options {\n    ...OptionFragment\n    __typename\n  }\n  validationType\n  flattenedDefaultNodes {\n    __typename\n    ... on DefaultOption {\n      parentId\n      id\n      name\n      nextCursor\n      displayString\n      unitAmount\n      currency\n      decimalPlaces\n      selectedQuantity\n      caloricInfoDisplayString\n      defaultQuantity\n      isRequiredForOptionPromo\n      strikethroughPrice {\n        unitAmount\n        currency\n        displayString\n        symbol\n        decimalPlaces\n        __typename\n      }\n      dietaryTagsList {\n        type\n        abbreviatedTagDisplayString\n        fullTagDisplayString\n        __typename\n      }\n      imgUrl\n      chargeAbove\n      __typename\n    }\n    ... on DefaultOptionList {\n      parentId\n      id\n      name\n      subtitle\n      type\n      selectionNode\n      minNumOptions\n      maxNumOptions\n      minAggregateOptionsQuantity\n      maxAggregateOptionsQuantity\n      minOptionChoiceQuantity\n      maxOptionChoiceQuantity\n      numFreeOptions\n      isOptional\n      options {\n        id\n        name\n        unitAmount\n        currency\n        displayString\n        decimalPlaces\n        nextCursor\n        caloricInfoDisplayString\n        chargeAbove\n        defaultQuantity\n        isRequiredForOptionPromo\n        strikethroughPrice {\n          unitAmount\n          currency\n          displayString\n          symbol\n          decimalPlaces\n          __typename\n        }\n        dietaryTagsList {\n          type\n          abbreviatedTagDisplayString\n          fullTagDisplayString\n          __typename\n        }\n        imgUrl\n        __typename\n      }\n      __typename\n    }\n  }\n  __typename\n}\n\nfragment QuickAddContextFragment on QuickAddContext {\n  isEligible\n  price {\n    currency\n    decimalPlaces\n    displayString\n    sign\n    symbol\n    unitAmount\n    __typename\n  }\n  nestedOptions\n  specialInstructions\n  defaultQuantity\n  __typename\n}\n\nfragment RetailItemRatingFragment on RetailItemRating {\n  averageRating\n  displayNumRatings\n  numOfRatings\n  numOfReviews\n  highRatingThreshold\n  __typename\n}\n\nfragment RetailItemSwatchFragment on Swatch {\n  name\n  image\n  imageType\n  badges {\n    ...BadgeFragment\n    __typename\n  }\n  tag {\n    name\n    color\n    size\n    __typename\n  }\n  __typename\n}\n\nfragment PageInfoFragment on RetailPageInfo {\n  cursor\n  hasNextPage\n  __typename\n}\n\nfragment FacetV2Fragment on FacetV2 {\n  ...FacetV2BaseFragment\n  childrenMap {\n    ...FacetV2BaseFragment\n    __typename\n  }\n  __typename\n}\n\nfragment FacetV2BaseFragment on FacetV2 {\n  id\n  childrenCount\n  component {\n    ...FacetV2ComponentFragment\n    __typename\n  }\n  name\n  text {\n    ...FacetV2TextFragment\n    __typename\n  }\n  images {\n    main {\n      ...FacetV2ImageFragment\n      __typename\n    }\n    icon {\n      ...FacetV2ImageFragment\n      __typename\n    }\n    background {\n      ...FacetV2ImageFragment\n      __typename\n    }\n    accessory {\n      ...FacetV2ImageFragment\n      __typename\n    }\n    custom {\n      key\n      value {\n        ...FacetV2ImageFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  events {\n    click {\n      name\n      data\n      __typename\n    }\n    __typename\n  }\n  style {\n    spacing\n    background_color\n    border {\n      color\n      width\n      style\n      __typename\n    }\n    sizeClass\n    dlsType\n    __typename\n  }\n  layout {\n    omitFooter\n    gridSpecs {\n      Mobile {\n        ...FacetV2LayoutGridFragment\n        __typename\n      }\n      Phablet {\n        ...FacetV2LayoutGridFragment\n        __typename\n      }\n      Tablet {\n        ...FacetV2LayoutGridFragment\n        __typename\n      }\n      Desktop {\n        ...FacetV2LayoutGridFragment\n        __typename\n      }\n      WideScreen {\n        ...FacetV2LayoutGridFragment\n        __typename\n      }\n      UltraWideScreen {\n        ...FacetV2LayoutGridFragment\n        __typename\n      }\n      __typename\n    }\n    dlsPadding {\n      top\n      right\n      bottom\n      left\n      __typename\n    }\n    __typename\n  }\n  custom\n  logging\n  __typename\n}\n\nfragment FacetV2ComponentFragment on FacetV2Component {\n  id\n  category\n  __typename\n}\n\nfragment FacetV2TextFragment on FacetV2Text {\n  title\n  titleTextAttributes {\n    textStyle\n    textColor\n    __typename\n  }\n  subtitle\n  subtitleTextAttributes {\n    textStyle\n    textColor\n    __typename\n  }\n  accessory\n  accessoryTextAttributes {\n    textStyle\n    textColor\n    __typename\n  }\n  description\n  descriptionTextAttributes {\n    textStyle\n    textColor\n    __typename\n  }\n  custom {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment FacetV2ImageFragment on FacetV2Image {\n  uri\n  videoUri\n  placeholder\n  local\n  style\n  logging\n  events {\n    click {\n      name\n      data\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FacetV2LayoutGridFragment on FacetV2LayoutGrid {\n  interRowSpacing\n  interColumnSpacing\n  minDimensionCount\n  __typename\n}\n\nfragment RetailFilterFragment on RetailFilter {\n  id\n  name\n  type\n  key\n  iconType\n  selectionType\n  groupId\n  __typename\n}\n\nfragment RetailPillFilterFragment on PillFilter {\n  id\n  name\n  type\n  rangeDirection\n  radioGroupId\n  logging\n  allowedValues {\n    displayName\n    queryValue\n    __typename\n  }\n  icon {\n    name\n    color\n    __typename\n  }\n  backendFilterId\n  swatch {\n    ...RetailItemSwatchFragment\n    __typename\n  }\n  __typename\n}\n"
    custom_settings = {
        'HTTPCACHE_ENABLED':True
    }

    def start_requests(self):
        payload = { 
            "url": "https://www.doordash.com/convenience/store/29836339",
            "httpResponseBody": True,
            "followRedirect": True
        }
        yield scrapy.Request(
            'https://api.zyte.com/v1/extract',
            method='POST',
            headers=self.headers,
            body=json.dumps(payload),
            callback=self.parse_categories,
            dont_filter=True,
        )


    def load_data(self, response):
        return base64.b64decode(response.json()['httpResponseBody'])



    def parse_categories(self, response):
        response = scrapy.Selector(text=self.load_data(response))
        for category in response.css('[data-anchor-id="ConvenienceStorePageCarouselItem"]'):
            cat_id = category.css('a::attr(href)').get().split('/')[-1]
            data = {
                "operationName": "categorySearch",
                "variables": {
                    "storeId": "29836339",
                    "categoryId": cat_id,
                    "sortBysList": [
                        "UNSPECIFIED"
                    ],
                    "limit": 50,
                    "filterQuery": "",
                    "filterKeysList": [],
                    "aggregateStoreIds": []
                },
                "query": self.query
            }
            payload = {
                "url": "https://www.doordash.com/graphql/categorySearch?operation=categorySearch", 
                "httpResponseBody": True, 
                "httpRequestMethod": "POST", 
                "httpRequestText": json.dumps(data),
                 "customHttpRequestHeaders": [
                    {
                        "name": "Content-Type",
                        "value": "application/json",
                    },
                ],
            }
            yield scrapy.Request(
                'https://api.zyte.com/v1/extract',
                method='POST',
                headers=self.headers,
                body=json.dumps(payload),
                callback=self.parse_products,
                meta={'category': category.css('::attr(data-category-name)').get(), 'cat_id':cat_id},
                dont_filter=True,
            )

    def parse_products(self, response):
        data = json.loads(self.load_data(response))
        for item in data['data']['retailStoreCategoryFeed']['legoRetailItems']:
            item = json.loads(item['custom'])
            yield {
                'name':item['item_data']['item_name'],
                'description':item['logging']['description'],
                'price':item['item_data']['price']['display_string'],
                'category':response.meta['category']
            }

        if cursor := data['data']['retailStoreCategoryFeed']['pageInfo']['cursor']:
            data = {
                "operationName": "categorySearch",
                "variables": {
                    "storeId": "29836339",
                    "categoryId": response.meta['cat_id'],
                    "sortBysList": [
                        "UNSPECIFIED"
                    ],
                    "cursor": cursor,
                    "limit": 50,
                    "filterQuery": "",
                    "filterKeysList": [],
                    "aggregateStoreIds": []
                },
                "query": self.query
            }
            payload = {
                "url": "https://www.doordash.com/graphql/categorySearch?operation=categorySearch", 
                "httpResponseBody": True, 
                "httpRequestMethod": "POST", 
                "httpRequestText": json.dumps(data),
                 "customHttpRequestHeaders": [
                    {
                        "name": "Content-Type",
                        "value": "application/json",
                    },
                ],
            }
            yield scrapy.Request(
                'https://api.zyte.com/v1/extract',
                method='POST',
                headers=self.headers,
                body=json.dumps(payload),
                callback=self.parse_products,
                meta=response.meta,
                dont_filter=True,
            )
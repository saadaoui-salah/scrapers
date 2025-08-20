import scrapy
import json

QUERY = """query NotForSaleShopperPlatformFullRenderQuery($zpid: ID!, $altId: ID, $deviceType: deviceType, $deviceTypeV2: OmpV2DeviceInput, $useOmpV2: Boolean!) {
  property(zpid: $zpid, palsId: $altId) {
    ...DebugPanel_property
    ...NfsActionBarContent_property
    ...NfsMediaColumnContent_property
    ...NfsNavBarContent_property
    ...NfsSummaryContent_property
    ...NfsLightboxes_property
    ...NfsDataViewContent_property
    ...PageViewTracker_property
    ...UniversalAnalyticsDataLayerFragment_property
    ...NotForSaleSearchPageStateParams_property
    rentalMarketingTreatments
  }
  viewer {
    ...DebugPanel_viewer
    ...viewerManager_viewer
    ...NfsActionBarContent_viewer
    ...NfsLightboxes_viewer
    ...NfsDataViewContent_viewer
    ...PageViewTracker_viewer
  }
  abTests {
    ...abTestManager_abTests
    ...NfsDataViewContent_abTests
    ...NfsLightboxes_abTests
    ...UniversalAnalyticsDataLayerFragment_abTests
  }
}

fragment DebugPanel_property on Property {
  zpid
  listingSource
  listingAccount {
    zuid
    email
  }
  ownerAccount {
    zuid
  }
  lfaViewPropertyPageUrl
  listingOwnerConfigIDs
  postingPresentationTypes
  maloneId
}

fragment NfsActionBarContent_property on Property {
  ...ActionBarController_property
  ...ReleaseOwnership_property
  ...ClaimOwnership_property
  ...CSPropertyUpdatePage_property
  ...CSMoveHomeMapLocation_property
  ...PropertyEventLog_property
  ...EditPropertyHistory_property
  ...VerifyOwnership_property
  ...DsEditButton_property
}

fragment ActionBarController_property on Property {
  ...DsActionBar_property
}

fragment DsActionBar_property on Property {
  zpid
  city
  state
  homeStatus
  ...SaveHome_property
  ...SuperShareMenu_property
}

fragment SaveHome_property on Property {
  address {
    streetAddress
    city
    state
    zipcode
  }
  homeStatus
  isListingClaimedByCurrentSignedInUser
  isCurrentSignedInAgentResponsible
  zpid
  bedrooms
  bathrooms
  price
  yearBuilt
}

fragment SuperShareMenu_property on Property {
  ...Share_property
}

fragment Share_property on Property {
  zpid
  streetAddress
  city
  state
  zipcode
  homeStatus
  homeType
  bedrooms
  bathrooms
  livingAreaValue
  livingAreaUnitsShort
  address {
    streetAddress
    city
    state
    zipcode
  }
  attributionInfo {
    mlsId
    mlsName
    providerLogo
  }
  listing_sub_type {
    is_FSBA
    is_FSBO
    is_pending
    is_newHome
    is_foreclosure
    is_comingSoon
    is_bankOwned
    is_forAuction
  }
  responsivePhotos: photos {
    url
  }
}

fragment ReleaseOwnership_property on Property {
  zpid
  isListingClaimedByCurrentSignedInUser
  isCurrentSignedInUserVerifiedOwner
}

fragment ClaimOwnership_property on Property {
  zpid
  isListingClaimedByCurrentSignedInUser
  isCurrentSignedInUserVerifiedOwner
}

fragment CSPropertyUpdatePage_property on Property {
  propertyUpdatePageLink
}

fragment CSMoveHomeMapLocation_property on Property {
  moveHomeMapLocationLink
}

fragment PropertyEventLog_property on Property {
  propertyEventLogLink
}

fragment EditPropertyHistory_property on Property {
  editPropertyHistorylink
}

fragment VerifyOwnership_property on Property {
  zpid
  isCurrentSignedInUserVerifiedOwner
  isVerifiedClaimedByCurrentSignedInUser
}

fragment DsEditButton_property on Property {
  ...EditFactsLink_property
}

fragment EditFactsLink_property on Property {
  zpid
  listingDataSource
}

fragment NfsMediaColumnContent_property on Property {
  ...NfsMediaStream_property
  ...NfsPhotoCarousel_property
}

fragment NfsMediaStream_property on Property {
  responsivePhotos: photos {
    caption
    subjectType
    url
    mixedSources(aspectRatio: FourThirds) {
      jpeg {
        url
        width
      }
    }
  }
  ...StreetView_property
  ...StaticMap_property
}

fragment StreetView_property on Property {
  zpid
  longitude
  latitude
  hasBadGeocode
  isCamo
  listing_sub_type {
    is_FSBA
    is_newHome
  }
  streetViewMetadataUrlMediaWallLatLong: googleStreetViewMetadataSignedUrl(
    featureArea: "hdpMediaWall"
    locationType: LAT_LONG
  )
  streetViewMetadataUrlMediaWallAddress: googleStreetViewMetadataSignedUrl(
    featureArea: "hdpMediaWall"
    locationType: ADDRESS
  )
  streetViewServiceUrl(featureArea: "hdpMediaWall", width: 512, height: 234)
  streetView(featureArea: "hdpMediaWall") {
    addressSources(aspectRatio: EightThirds, minWidth: 150, maxWidth: 768) {
      width
      url
    }
    latLongSources(aspectRatio: EightThirds, minWidth: 150, maxWidth: 768) {
      width
      url
    }
  }
}

fragment StaticMap_property on Property {
  staticMap(
    featureArea: "hdpMediaWall"
    shouldGetAdditionalHighResSources: true
    zoom: 15
  ) {
    sources(aspectRatio: FourThirds, minWidth: 150, maxWidth: 768) {
      width
      url
      isHighResolutionStaticMap
    }
  }
}

fragment NfsPhotoCarousel_property on Property {
  ...getPhotoTiles_property
}

fragment getPhotoTiles_property on Property {
  responsivePhotos: photos {
    caption
    mixedSources(aspectRatio: FourThirds) {
      jpeg {
        url
        width
      }
      webp {
        url
        width
      }
    }
  }
}

fragment NfsNavBarContent_property on Property {
  ...NavBarController_property
}

fragment NavBarController_property on Property {
  ...DsNavBar_property
}

fragment DsNavBar_property on Property {
  topNavJson
}

fragment NfsSummaryContent_property on Property {
  ...NfsChip_property
}

fragment NfsChip_property on Property {
  ...FactsRow_property
  ...AddressRow_property
  ...StatusAndZestimateRow_property
  ...MortgageRow_property
}

fragment FactsRow_property on Property {
  ...BedBathBeyond_property
}

fragment BedBathBeyond_property on Property {
  bedrooms
  bathrooms
  livingArea
  homeType
  lotSize
  lotAreaValue
  lotAreaUnits
  livingAreaValue
  livingAreaUnitsShort
  state
  resoFacts {
    bathroomsFull
    bathroomsThreeQuarter
    bathroomsHalf
    bathroomsOneQuarter
  }
}

fragment AddressRow_property on Property {
  ...Address_property
}

fragment Address_property on Property {
  streetAddress
  city
  state
  zipcode
  isUndisclosedAddress
  formattedChip(xConsumerUsername: "hdp-web") {
    location {
      fullValue
    }
  }
}

fragment StatusAndZestimateRow_property on Property {
  zpid
  homeStatus
  zestimate
  rentZestimate
  currency
  hideZestimate
  dateSoldString
  taxAssessedValue
  taxAssessedYear
  ...StatusArea_property
}

fragment StatusArea_property on Property {
  homeStatus
  currency
  zipcode
  homeType
  contingentListingType
  attributionInfo {
    trueStatus
  }
  listing_sub_type {
    is_FSBA
    is_FSBO
    is_pending
    is_newHome
    is_bankOwned
    is_openHouse
    is_forAuction
    is_comingSoon
    is_foreclosure
  }
}

fragment MortgageRow_property on Property {
  country
  ...EstimatedPayment_property
}

fragment EstimatedPayment_property on Property {
  homeStatus
  price
  monthlyHoaFee
  mortgageZHLRates {
    thirtyYearFixedBucket {
      rate
      rateSource
      lastUpdated
    }
  }
  propertyTaxRate
  homeType
  listing_sub_type {
    is_forAuction
    is_FSBA
    is_FSBO
    is_pending
    is_comingSoon
    is_newHome
    is_foreclosure
    is_bankOwned
    is_openHouse
  }
  zipcode
  state
  country
  listingMetadata {
    FlexibleLayoutAB
  }
}

fragment NfsLightboxes_property on Property {
  ...ReportProblemLightbox_property
  ...Share_property
  ...MixedMediaLightbox_property
  ...MapLightboxContainer_property
}

fragment ReportProblemLightbox_property on Property {
  zpid
  homeStatus
}

fragment MixedMediaLightbox_property on Property {
  zpid
  homeStatus
  photoCount
  address {
    city
    state
    streetAddress
    zipcode
  }
  ...GalleryLightboxActionButtons_property
  ...SphereViewerContainer_property
  ...ShouldShowVideo_property
  ...ShouldShowVirtualTour_property
  ...VideoContainer_property
  ...GalleryLightboxFooter_property
  ...GalleryLightboxResponsiveGallery_property
  ...CommunityStyle_property
  ...GalleryLightboxThirdPartyVirtualTour_property
  ...GetShareWithCaseManagerEnabled_property
  responsivePhotosOriginalRatio: photos {
    caption
    mixedSources(aspectRatio: Original) {
      jpeg {
        url
        width
      }
      webp {
        url
        width
      }
    }
  }
  ...couldShowEmbeddedThirdPartyVirtualTour_property
}

fragment GalleryLightboxActionButtons_property on Property {
  zpid
  homeStatus
  isPremierBuilder
  address {
    streetAddress
    city
    state
    zipcode
  }
  ...SaveHome_property
  ...Variant_property
  ...HomeDetailsContactUpsell_property
}

fragment Variant_property on Property {
  isShowcaseListing
  isPremierBuilder
  homeStatus
  listing_sub_type {
    is_FSBO
    is_FSBA
    is_newHome
    is_foreclosure
    is_bankOwned
    is_forAuction
    is_comingSoon
  }
  zpid
  state
}

fragment HomeDetailsContactUpsell_property on Property {
  ...DsContactButtons_property
}

fragment DsContactButtons_property on Property {
  zpid
  listing_sub_type {
    is_FSBA
    is_FSBO
  }
  state
  ...DsGetAuctionDetailsButton_property
}

fragment DsGetAuctionDetailsButton_property on Property {
  postingUrl
}

fragment SphereViewerContainer_property on Property {
  ...SphereViewerListing_property
  ...SphereViewerAttribution_property
  ...SphereViewerVrModel_property
}

fragment SphereViewerListing_property on Property {
  streetAddress
  listingSubType: listing_sub_type {
    isFSBA: is_FSBA
    isPending: is_pending
    isNewHome: is_newHome
    isForeclosure: is_foreclosure
    isBankOwned: is_bankOwned
    isForAuction: is_forAuction
    isOpenHouse: is_openHouse
    isComingSoon: is_comingSoon
  }
  zpid
  hdpUrl
  tourViewCount
}

fragment SphereViewerAttribution_property on Property {
  postingContact {
    name
    photo(size: PROFILE_120_120) {
      url
    }
  }
}

fragment SphereViewerVrModel_property on Property {
  vrModel {
    vrModelGuid
    revisionId
  }
  richMedia {
    virtualTour {
      viewerUrl
      revisionId
    }
  }
}

fragment ShouldShowVideo_property on Property {
  homeStatus
  isZillowOwned
  hasPublicVideo
  primaryPublicVideo {
    sources {
      src
    }
  }
  richMediaVideos {
    mp4Url
    hlsUrl
  }
}

fragment ShouldShowVirtualTour_property on Property {
  homeStatus
  richMedia {
    virtualTour {
      viewerUrl
      revisionId
    }
  }
}

fragment VideoContainer_property on Property {
  ...VideoWalkthroughContainer_property
  ...GalleryLightboxHeaderMobile_property
}

fragment VideoWalkthroughContainer_property on Property {
  primaryPublicVideo {
    videoIdEncoded
    postingClient
    sourceVideoWidth
    sourceVideoHeight
    sources {
      presetName
      src
      type
    }
  }
  richMediaVideos {
    mp4Url
    hlsUrl
  }
}

fragment GalleryLightboxHeaderMobile_property on Property {
  ...SaveHome_property
}

fragment GalleryLightboxFooter_property on Property {
  ...GalleryLightboxHomeInfo_property
}

fragment GalleryLightboxHomeInfo_property on Property {
  price
  lastSoldPrice
  bedrooms
  bathrooms
  livingArea
  livingAreaValue
  livingAreaUnits
  homeStatus
  homeType
  currency
  listing_sub_type {
    is_newHome
    is_FSBO
    is_bankOwned
    is_foreclosure
    is_forAuction
    is_comingSoon
  }
  contingentListingType
  attributionInfo {
    trueStatus
  }
  isPremierBuilder
  newConstructionType
}

fragment GalleryLightboxResponsiveGallery_property on Property {
  homeStatus
  isPremierBuilder
  ...GalleryLightboxHeaderMobile_property
  ...GalleryLightboxActionButtons_property
  ...GalleryLightboxContactUpsell_property
}

fragment GalleryLightboxContactUpsell_property on Property {
  ...HomeDetailsContactUpsell_property
}

fragment GalleryLightboxThirdPartyVirtualTour_property on Property {
  thirdPartyVirtualTour {
    lightboxUrl
  }
  ...couldShowEmbeddedThirdPartyVirtualTour_property
}

fragment couldShowEmbeddedThirdPartyVirtualTour_property on Property {
  thirdPartyVirtualTour {
    lightboxUrl
  }
  ...couldShowThirdPartyVirtualTour_property
}

fragment couldShowThirdPartyVirtualTour_property on Property {
  homeStatus
  hasApprovedThirdPartyVirtualTourUrl
  thirdPartyVirtualTour {
    approved
  }
}

fragment CommunityStyle_property on Property {
  homeType
}

fragment GetShareWithCaseManagerEnabled_property on Property {
  isHousingConnector
  homeStatus
}

fragment MapLightboxContainer_property on Property {
  ...GalleryLightboxMapGoogle_property
}

fragment GalleryLightboxMapGoogle_property on Property {
  zpid
  streetAddress
  city
  state
  zipcode
  latitude
  longitude
  isUndisclosedAddress
  streetViewTileImageUrlMediumLatLong: googleStreetViewImageSignedUrl(
    featureArea: "hdpMediaWall"
    locationType: LAT_LONG
    width: 400
    height: 250
  )
  streetViewTileImageUrlMediumAddress: googleStreetViewImageSignedUrl(
    featureArea: "hdpMediaWall"
    locationType: ADDRESS
    width: 400
    height: 250
  )
  ...GalleryLightboxActionButtons_property
  ...GoogleStreetViewPanorama_property
  ...LotLinesMap_property
  ...GetShareWithCaseManagerEnabled_property
}

fragment LotLinesMap_property on Property {
  latitude
  longitude
  homeStatus
  zpid
  price
  thumb: photos(count: 1, size: THUMBNAIL) {
    url
  }
  neighborhoodMapThumb: photos(count: 1, size: S) {
    url
  }
}

fragment GoogleStreetViewPanorama_property on Property {
  zpid
  longitude
  latitude
  streetViewMetadataUrlMapLightboxAddress: googleStreetViewMetadataSignedUrl(
    featureArea: "hdpMapLightbox"
    locationType: ADDRESS
  )
}

fragment NfsDataViewContent_property on Property {
  stateId
  countyId
  cityId
  country
  isNonOwnerOccupied
  ...HomeValue_property
  ...NfsFactsAndFeatures_property
  ...NfsOverview_property
  ...DsPriceAndTaxHistory_property
  ...DsNeighborhood_property
  ...DsNearbySchools_property
  ...OmpDsNfsUpsellTop_property
  ...OmpDsNfsUpsellBottom_property
  ...OmpDsNfsUpsellRight_property
  ...WaysToSell_property
  ...OwnerOptions_property
  ...ContactAgentForm_property
  ...Tcos_property
  ...DsFooterSection_property
  ...DQFragment_property
  ...ComparableHomesModule_property
  ...ClaimsUpsell_property
  ...InlineSellerAttribution_property
  ...OmpV2WebOMHDPCombo_property
  ...OmpV2WebOMHDPBottom_property
}

fragment HomeValue_property on Property {
  country
  ...ZestimateSummary_property
}

fragment ZestimateSummary_property on Property {
  zpid
  homeStatus
  ...MessagePrompt_property
  ...PrimaryZestimate_property
  ...ZestimateForecast_property
  ...ZestimateChange_property
  ...ZestimateRange_property
  ...ZestimatePerSqft_property
}

fragment MessagePrompt_property on Property {
  zpid
  yearBuilt
  livingArea
  livingAreaValue
  bathrooms
  bedrooms
  homeType
  zestimate
  price
  homeStatus
  isListingClaimedByCurrentSignedInUser
}

fragment PrimaryZestimate_property on Property {
  zpid
  rentZestimate
  zestimate
  homeStatus
  listingDataSource
}

fragment ZestimateForecast_property on Property {
  zestimate
  forecast
}

fragment ZestimateChange_property on Property {
  zestimate
  zestimateMinus30
  rentZestimate
  restimateMinus30
}

fragment ZestimateRange_property on Property {
  zestimate
  zestimateLowPercent
  zestimateHighPercent
  rentZestimate
  restimateLowPercent
  restimateHighPercent
}

fragment ZestimatePerSqft_property on Property {
  homeType
  livingAreaValue
  livingAreaUnits
  lotAreaValue
  lotAreaUnits
}

fragment NfsFactsAndFeatures_property on Property {
  ...NfsFactsAndFeaturesCommon_property
  ...ServicesAvailability_property
}

fragment NfsFactsAndFeaturesCommon_property on Property {
  ...FactsAndFeaturesCommon_property
  ...EditFactsLink_property
  attributionInfo {
    listingAgreement
  }
  resoFacts {
    aboveGradeFinishedArea
    additionalParcelsDescription
    architecturalStyle
    belowGradeFinishedArea
    builderModel
    builderName
    buildingArea
    buildingAreaSource
    buildingFeatures
    constructionMaterials
    exteriorFeatures
    foundationDetails
    frontageLength
    frontageType
    hasAdditionalParcels
    hasPetsAllowed
    hasRentControl
    hasHomeWarranty
    inclusions
    incomeIncludes
    isNewConstruction
    listingTerms
    livingAreaRange
    livingAreaRangeUnits
    livingArea
    lotSizeDimensions
    numberOfUnitsVacant
    otherStructures
    ownership
    parcelNumber
    propertyCondition
    propertySubType
    structureType
    topography
    vegetation
    woodedArea
    yearBuiltEffective
  }
}

fragment FactsAndFeaturesCommon_property on Property {
  state
  currency
  homeStatus
  homeType
  resoFacts {
    accessibilityFeatures
    additionalFeeInfo
    associations {
      feeFrequency
      name
      phone
    }
    associationFee
    associationAmenities
    associationFee2
    associationFeeIncludes
    associationName
    associationName2
    associationPhone
    associationPhone2
    basementYN
    buildingName
    buyerAgencyCompensation
    buyerAgencyCompensationType
    appliances
    atAGlanceFacts {
      factLabel
      factValue
    }
    attic
    availabilityDate
    basement
    bathrooms
    bathroomsFull
    bathroomsHalf
    bathroomsOneQuarter
    bathroomsPartial
    bathroomsFloat
    bathroomsThreeQuarter
    bedrooms
    bodyType
    canRaiseHorses
    carportParkingCapacity
    cityRegion
    commonWalls
    communityFeatures
    compensationBasedOn
    contingency
    cooling
    coveredParkingCapacity
    cropsIncludedYN
    cumulativeDaysOnMarket
    developmentStatus
    doorFeatures
    electric
    elevation
    elevationUnits
    entryLevel
    entryLocation
    exclusions
    feesAndDues {
      type
      fee
      name
      phone
    }
    fencing
    fireplaceFeatures
    fireplaces
    flooring
    foundationArea
    furnished
    garageParkingCapacity
    gas
    greenBuildingVerificationType
    greenEnergyEfficient
    greenEnergyGeneration
    greenIndoorAirQuality
    greenSustainability
    greenWaterConservation
    hasAssociation
    hasAttachedGarage
    hasAttachedProperty
    hasCooling
    hasCarport
    hasElectricOnProperty
    hasFireplace
    hasGarage
    hasHeating
    hasLandLease
    hasOpenParking
    hasSpa
    hasPrivatePool
    hasView
    hasWaterfrontView
    heating
    highSchool
    highSchoolDistrict
    hoaFee
    hoaFeeTotal
    homeType
    horseAmenities
    horseYN
    interiorFeatures
    irrigationWaterRightsAcres
    irrigationWaterRightsYN
    isSeniorCommunity
    landLeaseAmount
    landLeaseExpirationDate
    laundryFeatures
    levels
    listingId
    lotFeatures
    lotSize
    livingQuarters {
      livingArea
      livingAreaUnits
      areaTotal
      areaTotalUnits
      features
      livingQuarterType
    }
    mainLevelBathrooms
    mainLevelBedrooms
    marketingType
    middleOrJuniorSchool
    middleOrJuniorSchoolDistrict
    municipality
    numberOfUnitsInCommunity
    offerReviewDate
    onMarketDate
    openParkingCapacity
    otherEquipment
    otherFacts {
      name
      value
    }
    otherParking
    ownershipType
    parkingCapacity
    parkingFeatures
    patioAndPorchFeatures
    poolFeatures
    pricePerSquareFoot
    roadSurfaceType
    roofType
    rooms {
      area
      description
      dimensions
      level
      features
      roomArea
      roomAreaSource
      roomAreaUnits
      roomDescription
      roomDimensions
      roomFeatures
      roomLength
      roomLengthWidthSource
      roomLengthWidthUnits
      roomLevel
      roomType
      roomWidth
    }
    securityFeatures
    sewer
    spaFeatures
    specialListingConditions
    stories
    storiesTotal
    subAgencyCompensation
    subAgencyCompensationType
    subdivisionName
    totalActualRent
    transactionBrokerCompensation
    transactionBrokerCompensationType
    utilities
    view
    waterSource
    waterBodyName
    waterfrontFeatures
    waterView
    waterViewYN
    windowFeatures
    yearBuilt
    zoning
    zoningDescription
  }
}

fragment ServicesAvailability_property on Property {
  ...TelecomAd_property
}

fragment TelecomAd_property on Property {
  adTargets
}

fragment NfsOverview_property on Property {
  description
  whatILove
  listingDataSource
  ...AsyncListingAttributionOverview_property
}

fragment AsyncListingAttributionOverview_property on Property {
  ...ListingAttributionOverview_property
}

fragment ListingAttributionOverview_property on Property {
  attributionInfo {
    agentEmail
    agentLicenseNumber
    agentName
    agentPhoneNumber
    attributionTitle
    brokerName
    brokerPhoneNumber
    buyerAgentMemberStateLicense
    buyerAgentName
    buyerBrokerageName
    coAgentLicenseNumber
    coAgentName
    coAgentNumber
    lastChecked
    lastUpdated
    listingOffices {
      associatedOfficeType
      officeName
    }
    listingAgents {
      associatedAgentType
      memberFullName
      memberStateLicense
    }
    mlsDisclaimer
    mlsId
    mlsName
    providerLogo
  }
  listing_sub_type {
    is_FSBO
  }
  listingMetadata {
    mustAttributeOfficeNameBeforeAgentName
    mustDisplayAttributionListAgentEmail
    mustDisplayAttributionListAgentPhone
    mustDisplayAttributionListingOfficePhone
    mustDisplayDisclaimerBelowAttribution
    mustHighlightAgentName
    mustHighlightListOfficeName
    mustMakeListingAgentContactable
  }
  pals {
    name
    palsId
  }
  resoFacts {
    listAOR
  }
  ...SellerAttribution_property
}

fragment SellerAttribution_property on Property {
  ...ListedBy_property
}

fragment ListedBy_property on Property {
  zpid
  listedBy {
    id
    elements {
      id
      text
      action {
        variant
        url
      }
    }
    textStyle
  }
}

fragment DsNeighborhood_property on Property {
  adTargets
  ...DsNeighborhoodIncludingNearbyHomes_property
}

fragment DsNeighborhoodIncludingNearbyHomes_property on Property {
  ...DsNeighborhoodCommon_property
  nearbyHomes(count: 8) {
    ...DsMiniCardGallery_property
    ...DsMiniCardCarousel_property
  }
}

fragment DsNeighborhoodCommon_property on Property {
  homeStatus
  price
  rentZestimate
  zestimate
  homeValues {
    region {
      shortName
      link
      zhvi {
        yoy
        value
      }
      zhviForecast {
        value
      }
    }
  }
  address {
    zipcode
  }
  parentRegion {
    name
  }
}

fragment DsMiniCardGallery_property on Property {
  zpid
  ...DsMiniCard_property
}

fragment DsMiniCard_property on Property {
  miniCardPhotos: photos(count: 1, size: S) {
    url
  }
  ...DsMiniCardCommon_property
}

fragment DsMiniCardCommon_property on Property {
  price
  currency
  bedrooms
  bathrooms
  livingArea
  livingAreaValue
  livingAreaUnits
  livingAreaUnitsShort
  listingMetadata {
    comminglingCategoryIsRulesApplicable
  }
  resoFacts {
    bathroomsOneQuarter
    bathroomsHalf
    bathroomsThreeQuarter
    bathroomsFull
  }
  lotSize
  lotAreaValue
  lotAreaUnits
  address {
    streetAddress
    city
    state
    zipcode
  }
  parentRegion {
    name
  }
  formattedChip(xConsumerUsername: "hdp-web") {
    location {
      fullValue
    }
  }
  latitude
  longitude
  zpid
  homeStatus
  homeType
  hdpUrl
  hdpTypeDimension
  propertyTypeDimension
  listingTypeDimension
  listing_sub_type {
    is_newHome
    is_forAuction
    is_bankOwned
    is_foreclosure
    is_FSBO
    is_comingSoon
  }
  providerListingID
  attributionInfo {
    mlsId
    mlsName
    providerLogo
    agentName
    agentPhoneNumber
    brokerName
    brokerPhoneNumber
    trueStatus
  }
  ...Variant_property
  ...NcVariant_property
}

fragment NcVariant_property on Property {
  isPremierBuilder
  newConstructionType
}

fragment DsMiniCardCarousel_property on Property {
  zpid
  ...DsMiniCard_property
}

fragment DsNearbySchools_property on Property {
  country
  state
  schools {
    distance
    name
    rating
    level
    studentsPerTeacher
    assigned
    grades
    link
    type
    size
    totalCount
    assigned
    isAssigned
  }
  citySearchUrl {
    text
  }
  ...DsResoSchools_property
}

fragment DsResoSchools_property on Property {
  isPremierBuilder
  resoFacts {
    elementarySchool
    middleOrJuniorSchool
    highSchool
    elementarySchoolDistrict
  }
  attributionInfo {
    mlsName
  }
}

fragment DsPriceAndTaxHistory_property on Property {
  zpid
  countyFIPS
  parcelId
  taxHistory {
    time
    taxPaid
    taxIncreaseRate
    value
    valueIncreaseRate
  }
  priceHistory {
    date
    time
    price
    pricePerSquareFoot
    priceChangeRate
    event
    source
    buyerAgent {
      photo {
        url
      }
      profileUrl
      name
    }
    sellerAgent {
      photo {
        url
      }
      profileUrl
      name
    }
    showCountyLink
    postingIsRental
    attributeSource {
      infoString1
      infoString2
      infoString3
    }
  }
  currency
  country
  listing_sub_type {
    is_forAuction
    is_comingSoon
  }
}

fragment OmpDsNfsUpsellTop_property on Property {
  zpid
  NFSHDPTopSlot: onsiteMessage(
    placementNames: ["NFSHDPTopSlot"]
    placementData: {deviceType: $deviceType}
  ) @skip(if: $useOmpV2) {
    ...onsiteMessage_fragment
  }
}

fragment onsiteMessage_fragment on OnsiteMessageResultType {
  eventId
  decisionContext
  messages {
    skipDisplayReason
    shouldDisplay
    isGlobalHoldout
    isPlacementHoldout
    placementName
    testPhase
    bucket
    placementId
    passThrottle
    lastModified
    eventId
    decisionContext
    selectedTreatment {
      id
      name
      component
      status
      renderingProps
      lastModified
    }
    qualifiedTreatments {
      id
      name
      status
      lastModified
    }
  }
}

fragment OmpDsNfsUpsellBottom_property on Property {
  zpid
  NFSHDPBottomSlot: onsiteMessage(
    placementNames: ["NFSHDPBottomSlot"]
    placementData: {deviceType: $deviceType}
  ) @skip(if: $useOmpV2) {
    ...onsiteMessage_fragment
  }
}

fragment OmpDsNfsUpsellRight_property on Property {
  zpid
  NFSHDPRightRail: onsiteMessage(
    placementNames: ["NFSHDPRightRail"]
    placementData: {deviceType: $deviceType}
  ) @skip(if: $useOmpV2) {
    ...onsiteMessage_fragment
  }
}

fragment WaysToSell_property on Property {
  zpid
}

fragment OwnerOptions_property on Property {
  zpid
  zipcode
  zestimate
  rentZestimate
  currency
  price
  propertyTaxRate
  hoaFee
  adTargets
  mortgageRates {
    thirtyYearFixedRate
  }
}

fragment ContactAgentForm_property on Property {
  streetAddress
  state
  city
  zipcode
  zpid
  homeStatus
  homeType
  zestimate
  homeType
  isInstantOfferEnabled
  zillowOfferMarket {
    name
    code
  }
}

fragment Tcos_property on Property {
  zpid
  zestimate
  dateSold
  lastSoldPrice
  price
  city
  state
  county
  homeStatus
}

fragment DsFooterSection_property on Property {
  zpid
  isRentalListingOffMarket
  ...Comscore_property
  ...DsHomeDetailsFooter_property
  ...DsBreadcrumbs_property
  adTargets
}

fragment Comscore_property on Property {
  zpid
  address {
    streetAddress
    state
    city
    zipcode
  }
  hdpUrl
}

fragment DsHomeDetailsFooter_property on Property {
  listing_sub_type {
    is_newHome
  }
  ...NearbyCitiesColumn_property
  ...NearbyNeighborhoodsColumn_property
  ...NearbyZipcodesColumn_property
  ...OtherTopicsColumn_property
  ...DsBreadcrumbs_property
  ...CityApartmentsForRentSRPsColumn_property
}

fragment NearbyCitiesColumn_property on Property {
  nearbyCities {
    regionUrl {
      path
    }
    name
    body {
      city
      state
    }
  }
}

fragment NearbyNeighborhoodsColumn_property on Property {
  nearbyNeighborhoods {
    regionUrl {
      path
    }
    name
    body {
      neighborhood
      city
      state
    }
  }
}

fragment NearbyZipcodesColumn_property on Property {
  country
  nearbyZipcodes {
    regionUrl {
      path
    }
    name
    body {
      zipcode
      city
      state
    }
  }
}

fragment OtherTopicsColumn_property on Property {
  city
  state
  zipcode
  cityId
  citySearchUrl {
    text
    path
  }
  zipcodeSearchUrl {
    path
  }
  apartmentsForRentInZipcodeSearchUrl {
    path
  }
  housesForRentInZipcodeSearchUrl {
    path
  }
}

fragment DsBreadcrumbs_property on Property {
  ...Breadcrumbs_property
}

fragment Breadcrumbs_property on Property {
  streetAddress
  abbreviatedAddress
  city
  state
  county
  zipcode
  address {
    neighborhood
    community
    subdivision
  }
  neighborhoodRegion {
    name
  }
  building {
    bdpUrl
    buildingName
  }
  isUndisclosedAddress
  boroughId
  providerListingID
  neighborhoodSearchUrl {
    path
  }
  stateSearchUrl {
    path
  }
  countySearchUrl {
    text
    path
  }
  citySearchUrl {
    text
    path
  }
  zipcodeSearchUrl {
    path
  }
  boroughSearchUrl {
    text
    path
  }
  communityUrl {
    path
  }
  ...Variant_property
}

fragment CityApartmentsForRentSRPsColumn_property on Property {
  city
  state
  homeType
}

fragment ComparableHomesModule_property on Property {
  ...CompsModule_property
}

fragment CompsModule_property on Property {
  homeValuation(xConsumerUsername: "omhdp") {
    comparables {
      comps {
        property {
          ...CompsCarouselPropertyCard_property
          ...CompsMapSection_property
        }
      }
    }
  }
  ...CompsCarouselPropertyCard_property
  ...CompsMapSection_property
}

fragment CompsCarouselPropertyCard_property on Property {
  zestimate
  lastSoldPrice
  price
  daysOnZillow
  dateSold
  currency
  bedrooms
  bathrooms
  livingAreaValue
  livingAreaUnits
  livingAreaUnitsShort
  lotAreaValue
  lotAreaUnits
  address {
    streetAddress
    city
    state
    zipcode
  }
  latitude
  longitude
  zpid
  homeStatus
  homeType
  hdpUrl
  listing_sub_type {
    is_newHome
    is_forAuction
    is_bankOwned
    is_foreclosure
    is_FSBO
    is_comingSoon
  }
  isUndisclosedAddress
  attributionInfo {
    mlsId
    mlsName
    providerLogo
    agentName
    agentPhoneNumber
    brokerName
    brokerPhoneNumber
  }
  compsCarouselPropertyPhotos: photos(count: 1, size: S) {
    mixedSources(aspectRatio: FourThirds) {
      jpeg {
        url
      }
    }
  }
}

fragment CompsMapSection_property on Property {
  latitude
  longitude
}

fragment DQFragment_property on Property {
  listingMetadata {
    FlexibleLayoutB
    FlexibleLayoutC
    FlexibleLayoutD
    FlexibleLayoutE
    FlexibleLayoutF
    FlexibleLayoutG
    FlexibleLayoutH
    FlexibleLayoutI
    FlexibleLayoutJ
    FlexibleLayoutK
    FlexibleLayoutL
    FlexibleLayoutM
    FlexibleLayoutN
    FlexibleLayoutO
    FlexibleLayoutP
    FlexibleLayoutQ
    FlexibleLayoutR
    FlexibleLayoutS
    FlexibleLayoutT
    FlexibleLayoutU
    FlexibleLayoutV
    FlexibleLayoutW
    FlexibleLayoutX
    FlexibleLayoutY
    FlexibleLayoutZ
    FlexibleLayoutAA
    FlexibleLayoutAB
    passwordRequiredForZestimateMarketAnalysis
    canShowAutomatedValuationDisplay
    canShowTaxHistory
    canShowPriceHistory
    canShowUserGeneratedContent
    isAdsRestricted
    hidePriceAdjustmentFlexField
    canCommingleComparables
    canShowComparables
    isSuperTrafficOptimized
    mustDisplayDisclaimerBelowAttribution
    mustDisplayFeedLogoInContactBox
    canShowCroppedPhotos
    canShowNonIDXMedia
    canShowOnMap
    comminglingCategory
    mustDisplayAttributionAboveLocalFacts
    mustDisplayAttributionListAgentEmail
    mustDisplayAttributionListAgentPhone
    mustDisplayAttributionListingOfficePhone
    mustDisplayAuctionStatusAsSold
    mustHighlightAgentName
    mustHighlightMlsId
    mustHighlightMlsStatus
    mustHighlightListOfficeName
    mustMakeListingAgentContactable
    mustHighlightMarketingType
    mustAttributeOfficeNameBeforeAgentName
    canShowZillowLogoInHeader
    canShowPrequalifiedLinkInChip
    comminglingCategoryIsRulesApplicable
  }
}

fragment ClaimsUpsell_property on Property {
  zpid
  isConfirmedClaimedByCurrentSignedInUser
  isVerifiedClaimedByCurrentSignedInUser
}

fragment InlineSellerAttribution_property on Property {
  ...ListedBy_property
}

fragment OmpV2WebOMHDPCombo_property on Property {
  zpid
  OmpV2WebOMHDPCombo: ompV2Message(
    placementGroup: WEB_OMHDP_COMBO
    config: {deviceType: $deviceTypeV2, placementSupportedComponents: [{placementName: WEB_OMHDP_TOP_SLOT, supportedComponents: [OmpV2WebUpsellCard, OmpV2WebEmphasizedUpsellCard]}, {placementName: WEB_OMHDP_RIGHT_RAIL, supportedComponents: [OmpV2WebEmphasizedUpsellCard]}, {placementName: WEB_OMHDP_MOBILE_FOOTER, supportedComponents: [OmpV2WebButtonUpsellCard]}]}
  ) @include(if: $useOmpV2) {
    placementGroupDecision {
      eventId
      placementGroup
      experienceType
      experienceName
      error {
        message
      }
      placementDecisions {
        placementName
        selectedMessage {
          id
          name
          component {
            __typename
            ... on OmpV2WebEmphasizedUpsellCard {
              emphasizedHeader: header
              emphasizedBody: body {
                beforeText
                afterText
                tooltip {
                  trigger
                  title
                  subTitle
                  content
                  actionText
                  actionUrl
                }
              }
              primarySection {
                label {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                value {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                hasDivider
              }
              secondarySection {
                label {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                value {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                hasDivider
              }
              tertiarySection {
                label {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                value {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                hasDivider
              }
              primaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              isNarrowContainer
            }
            ... on OmpV2WebUpsellCard {
              simpleHeader: header
              simpleBody: body
              primaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              secondaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              imageMedia {
                src
                alt
                width
                height
              }
              advertisementText
              advertisementMedia {
                src
                alt
                width
                height
              }
              hasBorder
              dismissible
              backgroundColor
              mlsText
            }
            ... on OmpV2WebButtonUpsellCard {
              requiredCTA: primaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              secondaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
            }
          }
        }
        eventMetadata {
          exposureBlock {
            randomizationKey
            keyTypeCd
            decisionToken
            assignmentServiceCd
            treatments
            extendedInfo {
              key
              value
            }
          }
          nbaBlock {
            isNbaProcessed
            surfaceId
            position
            joiningUuid
            serviceErrorInd
            serviceErrorTxt
            selectedActionPositions {
              key
              value
            }
            userImpressionReportedInd
            fallBackActionRankingUsedInd
            selectedFallBackActions {
              key
              value
            }
          }
          ompV2Block {
            eventId
            placementName
            placementGroup
            assignedExperienceType
            selectedExperienceType
            selectedExperienceName
            selectedExperienceTrial
            selectedExperienceTrialAssignment
            qualifiedNbaActions
            selectedNbaAction
            qualifiedNbaMessages
            selectedNbaMessage
            selectedMessage
            selectedMessageAttributions
            qualifiedExperiencesMultivariateName
            qualifiedExperiencesDefaultName
            qualifiedExperiencesNbaName
          }
        }
      }
    }
  }
}

fragment OmpV2WebOMHDPBottom_property on Property {
  zpid
  OmpV2WebOMHDPBottom: ompV2Message(
    placementGroup: WEB_OMHDP_BOTTOM
    config: {deviceType: $deviceTypeV2, placementSupportedComponents: [{placementName: WEB_OMHDP_BOTTOM_SLOT, supportedComponents: [OmpV2WebUpsellCard, OmpV2WebEmphasizedUpsellCard]}]}
  ) @include(if: $useOmpV2) {
    placementGroupDecision {
      eventId
      placementGroup
      experienceType
      experienceName
      error {
        message
      }
      placementDecisions {
        placementName
        selectedMessage {
          id
          name
          component {
            __typename
            ... on OmpV2WebEmphasizedUpsellCard {
              emphasizedHeader: header
              emphasizedBody: body {
                beforeText
                afterText
                tooltip {
                  trigger
                  title
                  subTitle
                  content
                  actionText
                  actionUrl
                }
              }
              primarySection {
                label {
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                value {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                hasDivider
              }
              secondarySection {
                label {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                value {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                hasDivider
              }
              tertiarySection {
                label {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                value {
                  __typename
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionText {
                    text
                    subText
                    fontColor
                    fontType
                  }
                  ... on OmpV2WebEmphasizedUpsellCardValueSectionTooltip {
                    trigger
                    title
                    subTitle
                    content
                    actionText
                    actionUrl
                  }
                }
                hasDivider
              }
              primaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              isNarrowContainer
            }
            ... on OmpV2WebUpsellCard {
              simpleHeader: header
              simpleBody: body
              primaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              secondaryCTA {
                ctaUrl
                ctaText
                ctaButtonStyle
                ctaSubText
              }
              imageMedia {
                src
                alt
                width
                height
              }
              advertisementText
              advertisementMedia {
                src
                alt
                width
                height
              }
              hasBorder
              dismissible
              backgroundColor
              mlsText
            }
          }
        }
        eventMetadata {
          exposureBlock {
            randomizationKey
            keyTypeCd
            decisionToken
            assignmentServiceCd
            treatments
            extendedInfo {
              key
              value
            }
          }
          nbaBlock {
            isNbaProcessed
            surfaceId
            position
            joiningUuid
            serviceErrorInd
            serviceErrorTxt
            selectedActionPositions {
              key
              value
            }
            userImpressionReportedInd
            fallBackActionRankingUsedInd
            selectedFallBackActions {
              key
              value
            }
          }
          ompV2Block {
            eventId
            placementName
            placementGroup
            assignedExperienceType
            selectedExperienceType
            selectedExperienceName
            selectedExperienceTrial
            selectedExperienceTrialAssignment
            qualifiedNbaActions
            selectedNbaAction
            qualifiedNbaMessages
            selectedNbaMessage
            selectedMessage
            selectedMessageAttributions
            qualifiedExperiencesMultivariateName
            qualifiedExperiencesDefaultName
            qualifiedExperiencesNbaName
          }
        }
      }
    }
  }
}

fragment PageViewTracker_property on Property {
  zpid
  address {
    streetAddress
    state
    city
    zipcode
    neighborhood
  }
  zestimate
  hdpUrl
  price
  homeType
  homeStatus
  listing_sub_type {
    is_pending
    is_comingSoon
    is_FSBO
    is_bankOwned
    is_newHome
    is_foreclosure
    is_forAuction
    is_FSBA
  }
  isRecentStatusChange
  isNonOwnerOccupied
  brokerId
  ssid
  buildingId
  county
  newConstructionType
  daysOnZillow
  latitude
  longitude
  bedrooms
  bathrooms
  livingArea
  livingAreaValue
  lotSize
  lotAreaValue
  yearBuilt
  foreclosureTypes {
    isBankOwned
    wasNonRetailAuction
    wasDefault
  }
  isFeatured
  postingUrl
  providerListingID
  isPremierBuilder
  rentalApplicationsAcceptedType
  brokerageName
  currency
  propertyTypeDimension
  hdpTypeDimension
  listingTypeDimension
  featuredListingTypeDimension
  brokerIdDimension
  keystoneHomeStatus
  pageUrlFragment
  contingentListingType
  isRentalsLeadCapMet
  isPaidMultiFamilyBrokerId
  timeZone
  resoFacts {
    otherFacts {
      value
      name
    }
  }
  tourEligibility(
    platform: WEB
    useAsyncAb: false
    supportedTourTypes: [STANDARD, INSTANT, INSTANT_BOOK]
  ) {
    isPropertyTourEligible
  }
  virtualTourUrl
  bedrooms
  bathrooms
  ...IMXRichMedia_property
  ...NcVariant_property
  ...ShouldShowFloorMap_property
  ...ShouldShowVideo_property
  ...ShouldShowVirtualTour_property
  ...couldShowThirdPartyVirtualTour_property
  ...couldShowEmbeddedThirdPartyVirtualTour_property
}

fragment IMXRichMedia_property on Property {
  richMedia {
    imx {
      viewerUrl
      revisionId
      hasLocalizedPhotos
      isLmsTour
    }
  }
}

fragment ShouldShowFloorMap_property on Property {
  homeStatus
  richMedia {
    floorPlan {
      viewerUrl
    }
  }
}

fragment UniversalAnalyticsDataLayerFragment_property on Property {
  ...PropertyInfoBlockFragment_property
  ...Variant_property
}

fragment PropertyInfoBlockFragment_property on Property {
  zpid
  buildingId
  virtualTourUrl
  isPremierBuilder
  isShowcaseListing
  thirdPartyVirtualTour {
    providerKey
  }
  ...ShouldShowVirtualTour_property
  ...IMXRichMedia_property
  ...IMXLightboxEntryFragments_property
}

fragment IMXLightboxEntryFragments_property on Property {
  isShowcaseListing
  ...IMXPhotoView_property
  ...IMXRichMedia_property
  ...IMXViewContainer_property
  ...IMXViewMenu_property
  ...SphereViewerListing_property
}

fragment IMXPhotoView_property on Property {
  listingMetadata {
    mustPreferMlsPhotos
  }
  originalPhotos: photos {
    caption
    mixedSources(aspectRatio: Original) {
      jpeg {
        url
        width
      }
      webp {
        url
        width
      }
    }
  }
}

fragment IMXViewContainer_property on Property {
  bedrooms
  bathrooms
  contingentListingType
  homeStatus
  listingSubType: listing_sub_type {
    isFSBA: is_FSBA
    isFSBO: is_FSBO
    isPending: is_pending
    isNewHome: is_newHome
    isForeclosure: is_foreclosure
    isBankOwned: is_bankOwned
    isForAuction: is_forAuction
    isOpenHouse: is_openHouse
    isComingSoon: is_comingSoon
  }
  livingAreaValue
  price
  ...IMXAttribution_property
}

fragment IMXAttribution_property on Property {
  listingAccountUserId
  attributionInfo {
    agentName
    agentEmail
    agentPhoneNumber
    brokerName
    mlsId
  }
}

fragment IMXViewMenu_property on Property {
  isUndisclosedAddress
  address {
    streetAddress
    zipcode
    city
    state
  }
}

fragment NotForSaleSearchPageStateParams_property on Property {
  latitude
  longitude
  homeStatus
  cityId
  stateId
  boroughId
  countyId
}

fragment viewerManager_viewer on Viewer {
  displayName
  email
  emailHash
  isAdmin
  name
  roles {
    isAgent
  }
  zuid
}

fragment DebugPanel_viewer on Viewer {
  zuid
  isAdmin
}

fragment NfsActionBarContent_viewer on Viewer {
  ...ActionBarController_viewer
}

fragment ActionBarController_viewer on Viewer {
  ...DsActionBar_viewer
}

fragment DsActionBar_viewer on Viewer {
  email
  ...SuperShareMenu_viewer
}

fragment SuperShareMenu_viewer on Viewer {
  ...Share_viewer
}

fragment Share_viewer on Viewer {
  email
}

fragment NfsLightboxes_viewer on Viewer {
  ...ReportProblemLightbox_viewer
  ...MixedMediaLightbox_viewer
  ...MapLightboxContainer_viewer
}

fragment ReportProblemLightbox_viewer on Viewer {
  email
}

fragment MixedMediaLightbox_viewer on Viewer {
  ...GalleryLightboxActionButtons_viewer
  ...GalleryLightboxResponsiveGallery_viewer
  ...GetShareWithCaseManagerEnabled_viewer
}

fragment GalleryLightboxResponsiveGallery_viewer on Viewer {
  ...GalleryLightboxContactUpsell_viewer
}

fragment GalleryLightboxContactUpsell_viewer on Viewer {
  ...HomeDetailsContactUpsell_viewer
}

fragment HomeDetailsContactUpsell_viewer on Viewer {
  ...DsContactButtons_viewer
}

fragment DsContactButtons_viewer on Viewer {
  email
}

fragment GalleryLightboxActionButtons_viewer on Viewer {
  ...HomeDetailsContactUpsell_viewer
}

fragment GetShareWithCaseManagerEnabled_viewer on Viewer {
  roles {
    isLlpRenter
  }
}

fragment MapLightboxContainer_viewer on Viewer {
  ...GalleryLightboxMapGoogle_viewer
}

fragment GalleryLightboxMapGoogle_viewer on Viewer {
  ...GetShareWithCaseManagerEnabled_viewer
}

fragment NfsDataViewContent_viewer on Viewer {
  roles {
    isAgent
  }
  ...viewerManager_viewer
  ...ContactAgentForm_viewer
  ...DsFooterSection_viewer
}

fragment ContactAgentForm_viewer on Viewer {
  name
  email
  zuid
}

fragment DsFooterSection_viewer on Viewer {
  isAdmin
}

fragment PageViewTracker_viewer on Viewer {
  emailHash
}

fragment abTestManager_abTests on ABTests {
  AB_DASHBOARD_AA_TEST: abTest(trial: "AB_DASHBOARD_AA_TEST")
  ACTIVATION_ENABLED: abTest(trial: "Activation_Enabled")
  ACTIVATION_ONBOARDING: abTest(trial: "Activation_Onboarding")
  ACTIVATION_ONBOARDING_ENABLED: abTest(trial: "Activation_Onboarding_Enabled")
  ACTIVATION_GA_METRICS_ENABLED: abTest(trial: "Activation_GA_Metrics_Enabled")
  AIPERS_SIMILAR_HOMES_GDP: abTest(trial: "AIPERS_SIMILAR_HOMES_GDP")
  AR_CSAT_ONSITE_HDP: abTest(trial: "AR_CSAT_ONSITE_HDP")
  AR_CSAT_MODAL_HDP_LOAD_DELAY: abTest(trial: "AR_CSAT_MODAL_HDP_LOAD_DELAY")
  AR_SHOWCASE_HDP_WIDGET: abTest(trial: "AR_SHOWCASE_HDP_WIDGET")
  HDP_CONSTELLATION_PROPERTY_CARD: abTest(
    trial: "HDP_CONSTELLATION_PROPERTY_CARD"
  )
  HDP_DESKTOP_LAYOUT_TOPNAV: abTest(trial: "HDP_DESKTOP_LAYOUT_TOPNAV")
  HDP_EARLY_TRIAGE_REORDER: abTest(trial: "HDP_EARLY_TRIAGE_REORDER")
  HDP_EARLY_TRIAGE_REORDER_APP: abTest(trial: "HDP_EARLY_TRIAGE_REORDER_APP")
  HDP_FNF_BULLETS: abTest(trial: "HDP_FNF_BULLETS")
  HDP_HFF_ACCORDION: abTest(trial: "HDP_HFF_ACCORDION")
  HDP_HIGHLIGHT_OFFER_REVIEW: abTest(trial: "HDP_HIGHLIGHT_OFFER_REVIEW")
  HDP_HOLLYWOOD_FS_SUBTYPES: abTest(trial: "HDP_HOLLYWOOD_FS_SUBTYPES")
  HDP_HOME_INSIGHTS: abTest(trial: "HDP_HOME_INSIGHTS")
  HDP_INSIGHTS_VERSION: abTest(trial: "HDP_INSIGHTS_VERSION")
  HDP_REORDER_AT_A_GLANCE: abTest(trial: "HDP_REORDER_AT_A_GLANCE")
  HDP_SELLING_SOON_MSG: abTest(trial: "HDP_SELLING_SOON_MSG")
  HDP_SELLING_SOON_V2_TEST: abTest(trial: "HDP_SELLING_SOON_V2_TEST")
  HDP_TOP_SLOT: abTest(trial: "HDP_TOP_SLOT")
  HDP_UPDATED_FNF: abTest(trial: "HDP_UPDATED_FNF")
  HDP_ZHVI_CHART_MIGRATION: abTest(trial: "HDP_ZHVI_CHART_MIGRATION")
  MIGHTY_MONTH_2022_HOLDOUT: abTest(trial: "MIGHTY_MONTH_2022_HOLDOUT")
  MTT_GDP_PVS_CALL_GATE: abTest(trial: "MTT_GDP_PVS_CALL_GATE")
  NFSHDP_OWNER_OPTIONS_GOOGLE_AD: abTest(trial: "NFSHDP_OWNER_OPTIONS_GOOGLE_AD")
  PERF_DEFER_PHOTOS: abTest(trial: "PERF_DEFER_PHOTOS")
  PERF_PRELOAD_HDP_IMAGE: abTest(trial: "PERF_PRELOAD_HDP_IMAGE")
  RE_CANADA_CTA: abTest(trial: "RE_CANADA_CTA")
  RE_HDP_HOME_INSIGHTS: abTest(trial: "RE_HDP_HOME_INSIGHTS")
  RE_HDP_HOME_INSIGHTS_VERSION: abTest(trial: "RE_HDP_HOME_INSIGHTS_VERSION")
  RE_VARIANT_HDP_DEFERRED_HYDRATION: abTest(
    trial: "RE_VARIANT_HDP_DEFERRED_HYDRATION"
  )
  RE_NON_VARIANT_HDP_DEFERRED_HYDRATION: abTest(
    trial: "RE_NON_VARIANT_HDP_DEFERRED_HYDRATION"
  )
  SI_DownPaymentAssistance: abTest(trial: "SI_DownPaymentAssistance")
  SI_DPA_Apps: abTest(trial: "SI_DPA_Apps")
  SI_CostAndFees_HDP_Triage: abTest(trial: "SI_CostAndFees_HDP_Triage")
  SPT_RENDER_FOR_RENT_PAGE: abTest(trial: "SPT_RENDER_FOR_RENT_PAGE")
  TRACK_HOME_VALUE_V1: abTest(trial: "TRACK_HOME_VALUE_V1")
  UnassistedHomeShowingWeb: abTest(trial: "UnassistedHomeShowingWeb")
  SPT_RENDER_FOR_SALE_PAGE: abTest(trial: "SPT_RENDER_FOR_SALE_PAGE")
  VL_BDP_NEW_TAB: abTest(trial: "VL_BDP_NEW_TAB")
  HDP_NEW_ZESTIMATE_CHART: abTest(trial: "HDP_NEW_ZESTIMATE_CHART")
  ZEXP_HOLDOUT_ES_PILOT: abTest(trial: "ZEXP_HOLDOUT_ES_PILOT")
  ZHL_HDP_CHIP_PERSONALIZE_PAYMENT_CTAS: abTest(
    trial: "ZHL_HDP_CHIP_PERSONALIZE_PAYMENT_CTAS"
  )
  ZHL_HDP_CHIP_PERSONALIZE_PAYMENT_PERSISTENCE: abTest(
    trial: "ZHL_HDP_CHIP_PERSONALIZE_PAYMENT_PERSISTENCE"
  )
  ZHL_PERSONALIZED_PAYMENT_WEB_MVP: abTest(
    trial: "ZHL_PERSONALIZED_PAYMENT_WEB_MVP"
  )
  ZHL_PERSONALIZED_PAYMENT_MODULE: abTest(
    trial: "ZHL_PERSONALIZED_PAYMENT_MODULE"
  )
}

fragment NfsLightboxes_abTests on ABTests {
  ...MixedMediaLightbox_abTests
}

fragment MixedMediaLightbox_abTests on ABTests {
  RMX_LIGHTBOX_CHROME_1_5: abTest(trial: "RMX_LIGHTBOX_CHROME_1.5")
  ...SphereViewerContainer_abTests
  ...GalleryLightboxResponsiveGallery_abTests
  ...GalleryLightboxActionButtons_abTests
}

fragment SphereViewerContainer_abTests on ABTests {
  DELETE_WHEN_REAL_TRIAL_ADDED: abTest(trial: "DELETE_WHEN_REAL_TRIAL_ADDED")
}

fragment GalleryLightboxResponsiveGallery_abTests on ABTests {
  ...GalleryLightboxContactUpsell_abTests
}

fragment GalleryLightboxContactUpsell_abTests on ABTests {
  ...HomeDetailsContactUpsell_abTests
}

fragment HomeDetailsContactUpsell_abTests on ABTests {
  ...DsContactButtons_abTests
}

fragment DsContactButtons_abTests on ABTests {
  __typename
}

fragment GalleryLightboxActionButtons_abTests on ABTests {
  ...HomeDetailsContactUpsell_abTests
}

fragment NfsDataViewContent_abTests on ABTests {
  VSTA_NFS_HDP_HOLLYWOOD: abTest(trial: "VSTA_NFS_HDP_HOLLYWOOD")
  ZHL_PERSONALIZED_PAYMENT_MODULE: abTest(
    trial: "ZHL_PERSONALIZED_PAYMENT_MODULE"
  )
  Activation_Hollywood_Enabled: abTest(trial: "Activation_Hollywood_Enabled")
  Activation_Onboarding_Enabled: abTest(trial: "Activation_Onboarding_Enabled")
  ACTIVATION_UPSELL_CONTENT: abTest(trial: "ACTIVATION_UPSELL_CONTENT")
  SELLER_AGENT_SHOPPING_PILOT_WEB_TOF: abTest(
    trial: "SELLER_AGENT_SHOPPING_PILOT_WEB_TOF"
  )
  ...HomeValue_abTests
  ...abTestManager_abTests
  ...ClaimsUpsell_abTests
  ...ComparableHomesModule_abTests
  ...ContactAgentForm_abTests
  ...OwnerOptions_abTests
}

fragment HomeValue_abTests on ABTests {
  ...ZestimateSummary_abTests
}

fragment ZestimateSummary_abTests on ABTests {
  TRACK_HOME_VALUE_V1: abTest(trial: "TRACK_HOME_VALUE_V1")
  STABLE_HOME_VALUE_MODULE: abTest(trial: "STABLE_HOME_VALUE_MODULE")
}

fragment ClaimsUpsell_abTests on ABTests {
  NFSHDP_CLAIMS_UPSELL: abTest(trial: "NFSHDP_CLAIMS_UPSELL")
}

fragment ComparableHomesModule_abTests on ABTests {
  ...CompsModule_abTests
}

fragment CompsModule_abTests on ABTests {
  ...CompsMapSection_abTests
}

fragment CompsMapSection_abTests on ABTests {
  NFSHDP_COMPS_MODULE_MAP: abTest(trial: "NFSHDP_COMPS_MODULE_MAP")
}

fragment ContactAgentForm_abTests on ABTests {
  SHOW_PL_LEAD_FORM: abTest(trial: "SHOW_PL_LEAD_FORM")
}

fragment OwnerOptions_abTests on ABTests {
  NFSHDP_OWNER_OPTIONS_GOOGLE_AD: abTest(trial: "NFSHDP_OWNER_OPTIONS_GOOGLE_AD")
  NFSHDP_MST_WEB_PREBID_ARCANE: abTest(trial: "NFSHDP_MST_WEB_PREBID_ARCANE")
}

fragment UniversalAnalyticsDataLayerFragment_abTests on ABTests {
  ...PropertyInfoBlockFragment_abTests
  ...Variant_abTests
}

fragment PropertyInfoBlockFragment_abTests on ABTests {
  ...IMXLightboxEntryFragments_abTests
}

fragment IMXLightboxEntryFragments_abTests on ABTests {
  IMX_REPORT_PROBLEM: abTest(trial: "IMX_REPORT_PROBLEM")
  RMX_HIGH_RES_PHOTO: abTest(trial: "RMX_HIGH_RES_PHOTO")
  ...IMXViewContainer_abTests
  ...SphereViewerContainer_abTests
  ...IMXViewMenu_abTests
}

fragment IMXViewContainer_abTests on ABTests {
  ...IMXAttribution_abTests
}

fragment IMXAttribution_abTests on ABTests {
  DELETE_WHEN_REAL_TRIAL_ADDED: abTest(trial: "DELETE_WHEN_REAL_TRIAL_ADDED")
}

fragment IMXViewMenu_abTests on ABTests {
  GROUP_BY_ROOM_TOGGLE_IMX_LIGHTBOX: abTest(
    trial: "GROUP_BY_ROOM_TOGGLE_IMX_LIGHTBOX"
  )
}

fragment Variant_abTests on ABTests {
  SPT_RENDER_FOR_SALE_PAGE: abTest(trial: "SPT_RENDER_FOR_SALE_PAGE")
}
"""
payload = {
                "searchQueryState": {
                    "pagination": {
                        "currentPage": 1
                    },
                    "isMapVisible": True,
                    "mapBounds": {
                        "west": -81.47984554754879,
                        "east": -81.44598534094479,
                        "south": 28.31984241212324,
                        "north": 28.3497591218273
                    },
                    "mapZoom": 15,
                    "usersSearchTerm": "",
                    "filterState": {
                        "isForRent": {"value": True},
                        "isForSaleByAgent": {"value": False},
                        "isForSaleByOwner": {"value": False},
                        "isNewConstruction": {"value": False},
                        "isComingSoon": {"value": False},
                        "isAuction": {"value": False},
                        "isForSaleForeclosure": {"value": False}
                    },
                    "isListVisible": True
                },
                "wants": {
                    "cat1": ["listResults", "mapResults"]
                },
                "requestId": 1,
                "isDebugRequest": False
            }

payload = {
    "searchQueryState": {
        "pagination": {
            "currentPage": 3
        },
        "isMapVisible": True,
        "mapBounds": {
            "west": -81.49965097891476,
            "east": -81.43193056570675,
            "south": 28.300409306577784,
            "north": 28.36024524165079
        },
        "mapZoom": 14,
        "usersSearchTerm": "",
        "filterState": {
            "sortSelection": {
                "value": "globalrelevanceex"
            }
        },
        "isListVisible": True
    },
    "wants": {
        "cat1": [
            "listResults",
            "mapResults"
        ],
        "cat2": [
            "total"
        ]
    },
    "requestId": 4,
    "isDebugRequest": False
}

class ZillowSpider(scrapy.Spider):
    name = "zillow"
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "cookie": "zguid=24|%24ffb96bcd-01ed-4587-a154-e2486046e2bf; _ga=GA1.2.1920120732.1754435301; ...",  # shortened here
        "dnt": "1",
        "origin": "https://www.zillow.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        url = "https://www.zillow.com/async-create-search-page-state"
        for i in range(20):
            payload = {
                "searchQueryState": {
                    "pagination": {  "currentPage": i + 1},
                    "isMapVisible": True,
                    "mapBounds": {
                        "west": -81.50402834402706,
                        "east": -81.43630793081905,
                        "south": 28.305787717554836,
                        "north": 28.365620625013932
                    },
                    "mapZoom": 14,
                    "usersSearchTerm": "",
                    "filterState": {
                        "sortSelection": {
                            "value": "globalrelevanceex"
                        },
                        "isForSaleByAgent": {
                            "value": False
                        },
                        "isForSaleByOwner": {
                            "value": False
                        },
                        "isNewConstruction": {
                            "value": False
                        },
                        "isComingSoon": {
                            "value": False
                        },
                        "isAuction": {
                            "value": False
                        },
                        "isForSaleForeclosure": {
                            "value": False
                        },
                        "isRecentlySold": {
                            "value": True
                        }
                    },
                    "isListVisible": True
                },
                "wants": {
                    "cat1": [
                        "mapResults"
                    ]
                },
                "requestId": i+1,
                "isDebugRequest": False
            }
            
            yield scrapy.Request(
                url=url,
                method="PUT",
                headers=self.headers,
                body=json.dumps(payload),
                callback=self.parse
            )

    def parse(self, response):
        for listing in response.json()['cat1']['searchResults']['mapResults'] + response.json()['cat1']['searchResults']['listResults']:
            data = {
                'address': listing['address'],
                'zillow link': f"https://www.zillow.com{listing['detailUrl']}" if 'http' not in listing['detailUrl'] else listing['detailUrl']
            }
            try:
                url = f"https://www.zillow.com/graphql/?zpid={listing['zpid']}&altId=&deviceType=desktop&deviceTypeV2=WEB_DESKTOP&useOmpV2=false&operationName=NotForSaleShopperPlatformFullRenderQuery"
                payload = {
                    "operationName": "NotForSaleShopperPlatformFullRenderQuery",
                    "variables": {
                        "zpid": listing['zpid'],
                        "altId": None,
                        "deviceType": "desktop",
                        "deviceTypeV2": "WEB_DESKTOP",
                        "useOmpV2": False
                    },
                    "query": QUERY
                }
                
                yield scrapy.Request(
                    url=url,
                    method="POST",
                    headers=self.headers,
                    body=json.dumps(payload),
                    meta={'item': data},
                    callback=self.parse_details
                )
            except Exception as e:
                data['owner'] = 'N/A'
                data['mailing address'] = 'N/A'
                data['parcel number'] = 'N/A'
                yield data

    def parse_details(self, response):
        item = response.meta['item']
        try:
          parcel_id = response.json()['data']['property']['parcelId']
          item['parcel number'] = parcel_id
          yield scrapy.Request(
              url=f'https://search.property-appraiser.org/api/v1/ParcelMarket?$format=json&$top=20&$filter=contains(strap,%27{parcel_id}%27)&$count=true', 
              callback=self.parse_extra,
              dont_filter=True,
              meta=response.meta
              )
        except:
          item['owner'] = 'N/A'
          item['parcel number'] = 'N/A'
          item['mailing address'] = 'N/A'
          yield item

    def parse_extra(self, response):
        item = response.meta['item']
        try:
          data = response.json()['value'][0]
          item['owner'] = data['Owners']
          item['mailing address'] = data['Mailing']
        except IndexError:
          item['owner'] = 'N/A'
          item['mailing address'] = 'N/A'
        yield item
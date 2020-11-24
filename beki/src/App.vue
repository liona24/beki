<template>
  <div id="app">

    <section class="section">
      <div class="container is-max-desktop">
        <div class="box">
          <nav v-if="currentViewType !== ViewType.MainMenu" class="breadcrumb">
            <ul>
              <li v-for="(view, i) in views" :key="i">
                <a href="#">{{ breadcrumbForType(view.$type) }}</a>
              </li>
            </ul>
          </nav>

          <view-main-menu v-if="currentViewType === ViewType.MainMenu" />

          <view-protocol v-else-if="currentViewType === ViewType.Protocol" />

          <view-facility v-else-if="currentViewType === ViewType.Facility" />

          <view-organization v-else-if="currentViewType === ViewType.Organization" />

          <view-person v-else-if="currentViewType === ViewType.Person" />

          <view-inspection-standard v-else-if="currentViewType === ViewType.InspectionStandard" />

          <view-category v-else-if="currentViewType === ViewType.Category" />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import ViewMainMenu from './components/views/ViewMainMenu'
import ViewProtocol from './components/views/ViewProtocol'
import ViewFacility from './components/views/ViewFacility'
import ViewOrganization from './components/views/ViewOrganization'
import ViewPerson from './components/views/ViewPerson'
import ViewInspectionStandard from './components/views/ViewInspectionStandard'
import ViewCategory from './components/views/ViewCategory.vue'

import { ViewType } from './store/common'

import { mapGetters, mapState } from 'vuex'

export default {
  name: 'App',
  components: {
    ViewMainMenu,
    ViewProtocol,
    ViewInspectionStandard,
    ViewCategory,
    ViewPerson,
    ViewFacility,
    ViewOrganization,
  },
  computed: {
    ...mapState(['views']),
    ...mapGetters(['currentViewType']),
    ViewType() {
      return ViewType;
    }
  },
  methods: {
    breadcrumbForType(type) {
      switch (type) {
        case ViewType.MainMenu:
          return '#'
        case ViewType.Protocol:
          return 'Neu'
        case ViewType.Facility:
          return 'Objekt'
        case ViewType.Organization:
          return 'Organisation'
        case ViewType.Person:
          return 'Person'
        case ViewType.InspectionStandard:
          return 'Prüfkriterium'
        case ViewType.Category:
          return 'Kategorie'
        default:
          return ''
      }
    }
  }
}
</script>

<style>
</style>

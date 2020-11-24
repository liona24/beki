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

          <view-main-menu v-if="currentViewType === ViewType.MainMenu"> </view-main-menu>

          <view-protocol v-else-if="currentViewType === ViewType.Protocol"> </view-protocol>

          <template v-else-if="currentViewType === ViewType.Facility">
          </template>
          <template v-else-if="currentViewType === ViewType.Organization">
          </template>
          <template v-else-if="currentViewType === ViewType.Person">
          </template>
          <template v-else-if="currentViewType === ViewType.InspectionStandard">
          </template>
          <template v-else-if="currentViewType === ViewType.Category">
          </template>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import ViewMainMenu from './components/views/ViewMainMenu'
import ViewProtocol from './components/views/ViewProtocol'

import { ViewType } from './store/common'

import { mapGetters, mapState } from 'vuex'

export default {
  name: 'App',
  components: {
    ViewMainMenu,
    ViewProtocol
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

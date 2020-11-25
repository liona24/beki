<template>
  <div id="app">
    <b-navbar type="is-dark">
      <template slot="brand">
      </template>
      <template slot="start">
        <template v-for="(view, i) in views">
          <b-navbar-item :key="i + 'left'">
            <b-icon v-if="view.$type === ViewType.MainMenu" icon="home"> </b-icon>
            <template v-else> {{ breadcrumbForType(view.$type) }} </template>
          </b-navbar-item>
          <b-navbar-item :key="i + 'right'">
            <b-icon icon="chevron-right"></b-icon>
          </b-navbar-item>
        </template>
      </template>

      <template slot="end">
        <b-navbar-item v-if="currentViewType !== ViewType.MainMenu" tag="div">
            <div class="buttons">
              <a class="button is-light" @click="goBackWithPrompt">
                  Zurück
              </a>
            </div>
        </b-navbar-item>
      </template>
    </b-navbar>

    <!-- TODO: Snackbar notifications on error / success -->

    <section class="section">
      <div class="container is-max-desktop">
        <div class="box">
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

import { SyncStatus, ViewType } from './store/common'

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
    ...mapGetters(['currentViewType', 'currentView', 'currentStatus']),
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
          return 'Protokoll'
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
    },
    confirmGoBack(onConfirm) {
      this.$buefy.dialog.confirm({
        title: 'Änderungen verwerfen',
        message: 'Wenn du zuück gehst werden alle Änderungen <b>verworfen</b>. Letzte Chance?',
        confirmText: 'Verwerfen',
        cancelText: 'Abbrechen',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: onConfirm
      })
    },
    goBackWithPrompt() {
      if ((this.currentStatus & SyncStatus.Modified) !== 0) {
        this.confirmGoBack(this.goBack);
      } else {
        this.goBack();
      }
    },
    goBack() {
      this.$store.commit("pop", { discard: true });
    }
  }
}
</script>

<style>
</style>

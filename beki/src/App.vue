<template>
  <div id="app">
    <b-navbar type="is-dark">
      <template slot="brand">
      </template>
      <template slot="start">
        <template v-for="(view, i) in $store.state.main.views">
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
        <b-navbar-item v-if="mainViewType !== ViewType.MainMenu" tag="div">
            <div class="buttons">
              <a class="button is-light" @click="goBackWithPrompt">
                  Zurück
              </a>
            </div>
        </b-navbar-item>
      </template>
    </b-navbar>

    <section class="section">
      <div class="container is-max-desktop">
        <view-main-menu v-if="mainViewType === ViewType.MainMenu" />

        <view-protocol v-else-if="mainViewType === ViewType.Protocol" />

        <view-wizard v-else-if="mainViewType === ViewType.Wizard" />
      </div>
    </section>

    <div class="modal" :class="{ 'is-active': isOverlayActive }">
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="container is-max-desktop">
          <view-facility v-if="overlayViewType === ViewType.Facility" />

          <view-organization v-else-if="overlayViewType === ViewType.Organization" />

          <view-person v-else-if="overlayViewType === ViewType.Person" />

          <view-inspection-standard v-else-if="overlayViewType === ViewType.InspectionStandard" />

          <view-category v-else-if="overlayViewType === ViewType.Category" />
        </div>
      </div>
      <button class="modal-close is-large" aria-label="close" @click="closeOverlayWithPrompt"></button>
    </div>
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
import ViewWizard from './components/views/ViewWizard.vue'

import { SyncStatus, ViewType } from './store/common'

import { mapGetters } from 'vuex'

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
    ViewWizard,
  },
  data() {
    return {
      isCanceling: false,
    }
  },
  computed: {
    ...mapGetters(['mainViewType', 'main', 'mainStatus', 'overlayViewType', 'overlay', 'overlayStatus']),
    ViewType() {
      return ViewType;
    },
    isOverlayActive() {
      return this.overlayViewType !== undefined;
    }
  },
  methods: {
    breadcrumbForType(type) {
      switch (type) {
        case ViewType.MainMenu:
          return '#'
        case ViewType.Wizard:
          return 'Vorbereiten'
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
      if (this.isCanceling) {
        return;
      }

      this.isCanceling = true;

      this.$buefy.dialog.confirm({
        title: 'Änderungen verwerfen',
        message: 'Wenn du zuück gehst werden alle Änderungen <b>verworfen</b>. Letzte Chance?',
        confirmText: 'Verwerfen',
        cancelText: 'Abbrechen',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: e => {
          this.isCanceling = false;
          onConfirm(e);
        },
        onCancel: () => this.isCanceling = false
      });
    },
    goBackWithPrompt() {
      if ((this.mainStatus & SyncStatus.Modified) !== 0) {
        this.confirmGoBack(this.goBack);
      } else {
        this.goBack();
      }
    },
    goBack() {
      this.$store.dispatch("back_main", { discard: true });
    },
    closeOverlayWithPrompt() {
      if ((this.overlayStatus & SyncStatus.Modified) !== 0) {
        this.confirmGoBack(this.closeOverlay);
      } else {
        this.closeOverlay();
      }
    },
    closeOverlay() {
      this.$store.dispatch("back_overlay", { discard: true });
    },
    handleKeyPress({ key }) {
      if (this.mainViewType !== ViewType.MainMenu && key === "Escape" || key === "Esc") {
        if (this.isOverlayActive) {
          this.closeOverlayWithPrompt();
        } else {
          this.goBackWithPrompt();
        }
      }
    }
  },
  created() {
    if (typeof window !== 'undefined') {
      document.addEventListener('keyup', this.handleKeyPress);
    }
  },
  beforeDestroy() {
    if (typeof window !== 'undefined') {
      document.removeEventListener('keyup', this.handleKeyPress);
    }
  }
}
</script>

<style>
img {
  filter: drop-shadow(0.3em 0.3em 0.3em #22222254);
}

</style>

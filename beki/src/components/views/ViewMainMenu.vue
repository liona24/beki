<template>
  <b-loading v-if="isLoadingInternal" v-model="isLoadingInternal" :is-full-page="true" :can-cancel="false"></b-loading>
  <div v-else class="box">
    <b-tabs type="is-boxed">
      <!-- TODO: change highlight color -->
      <b-tab-item label="Neu" icon="file">
        <menu-create-new />
      </b-tab-item>
      <b-tab-item label="Bearbeiten" icon="pencil">
        <menu-edit />
      </b-tab-item>
      <b-tab-item label="Anzeigen" icon="magnify">
        <menu-search-and-display :legacy="false" />
      </b-tab-item>
      <b-tab-item label="Archiv" icon="package-variant">
        <menu-search-and-display :legacy="true" />
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import MenuSearchAndDisplay from '../content/menu/MenuSearchAndDisplay'
import MenuCreateNew from '../content/menu/MenuCreateNew'
import MenuEdit from '../content/menu/MenuEdit'
import { mapGetters } from 'vuex'

export default {
  name: "ViewMainMenu",
  components: { MenuSearchAndDisplay, MenuCreateNew, MenuEdit },
  data() {
    return {
      isLoadingInternal: false, // for some reason we need this for b-loading
    }
  },
  computed: {
    ...mapGetters('menu', ['isLoading', 'currentPreviewId'])
  },
  watch: {
    isLoading() {
      this.isLoadingInternal = this.isLoading;
    },
  },
  beforeMount() {
    if (this.currentPreviewId != null) {
      window.location.href = `/api/_render/${this.currentPreviewId}`
      // this.$store.commit("menu_currentPreview", { val: null });
    }
  }
}
</script>

<style>

</style>

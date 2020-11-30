<template>
  <b-loading v-if="isLoadingInternal" v-model="isLoadingInternal" :is-full-page="true" :can-cancel="false"></b-loading>
  <div v-else class="box">
    <b-tabs type="is-boxed">
      <!-- TODO: change highlight color -->
      <b-tab-item label="Anzeigen" icon="eye">
        <menu-search-and-display />
      </b-tab-item>
      <b-tab-item label="Neu" icon="file">
        <menu-create-new />
      </b-tab-item>
    </b-tabs>
  </div>
</template>

<script>
import MenuSearchAndDisplay from '../content/menu/MenuSearchAndDisplay'
import MenuCreateNew from '../content/menu/MenuCreateNew'
import { mapGetters } from 'vuex'

export default {
  name: "ViewMainMenu",
  components: { MenuSearchAndDisplay, MenuCreateNew },
  data() {
    return {
      isLoadingInternal: false, // for some reason we need this for b-loading
    }
  },
  computed: {
    ...mapGetters('menu', ['isLoading'])
  },
  watch: {
    isLoading() {
      this.isLoadingInternal = this.isLoading;
    }
  }
}
</script>

<style>

</style>

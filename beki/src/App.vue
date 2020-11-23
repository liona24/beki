<template>
  <div id="app">

    <section class="section">
      <div class="container is-max-desktop">

        <template v-if="state === 'MAIN_MENU'">
          <div class="box">
            <b-tabs size="is-medium" type="is-boxed">
                <b-tab-item label="Anzeigen" icon="eye">
                  <menu-search-and-display />
                </b-tab-item>
                <b-tab-item label="Neu" icon="file">
                  <menu-create-new />
                </b-tab-item>
            </b-tabs>
          </div>
        </template>

        <editor-protocol v-else-if="state === 'SHOW_EDITOR'" />

      </div>
    </section>
  </div>
</template>

<script>
import EditorProtocol from './components/editor/EditorProtocol.vue'
import MenuCreateNew from './components/menu/MenuCreateNew'
import MenuSearchAndDisplay from './components/menu/MenuSearchAndDisplay'

export default {
  name: 'App',
  components: {
    MenuCreateNew,
    MenuSearchAndDisplay,
    EditorProtocol
  },
  data() {
    return {
      state: "SHOW_EDITOR"
    }
  }
}
</script>

<style>
</style>

<template>
  <div id="app">

    <section class="section">
      <div class="container">
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
      </div>
    </section>
  </div>
</template>

<script>
import MenuCreateNew from './components/menu/MenuCreateNew'
import MenuSearchAndDisplay from './components/menu/MenuSearchAndDisplay'

export default {
  name: 'App',
  components: {
    MenuCreateNew,
    MenuSearchAndDisplay
  }
}
</script>

<style>
</style>

<template>
  <div>
    <b-field>
      <b-upload
        :value="droppedFiles"
        @input="updateDroppedFiles"
        accept="image/*"
        multiple
        drag-drop
        expanded>
        <section class="section">
            <div class="content has-text-centered">
                <p>
                  <b-icon
                      icon="upload"
                      size="is-large">
                  </b-icon>
                </p>
                <p>Bilder zum Hinzufügen hereinziehen</p>
            </div>
        </section>
      </b-upload>
    </b-field>

    <div class="block">
      <b-collapse v-show="droppedFiles.length > 0" class="card" animation="slide" :open="false" aria-id="contentIdForA11y3">
        <div
          slot="trigger"
          slot-scope="props"
          class="card-header"
          role="button"
          aria-controls="contentIdForA11y3">
          <p class="card-header-title">
            {{ droppedFiles.length }} Bild(er) ausgewählt
          </p>
          <a class="card-header-icon">
            <b-icon
              :icon="props.open ? 'menu-down' : 'menu-up'">
            </b-icon>
          </a>
        </div>
        <div class="card-content" style="overflow-x: auto">
          <div class="tile is-ancestor" v-show="!isPreviewLoading">
            <div v-for="(img, name) in previewImages" class="tile is-parent" :key="name">
              <div class="tile is-child box">
                <b-tooltip position="is-bottom" type="is-light" always>
                  <template slot="content">
                    {{ name }}
                    <button class="delete is-small"
                          type="button"
                          @click="deleteDropFile(name)">
                    </button>
                  </template>
                  <figure class="image is-128x128">
                    <img :src="img" />
                  </figure>
                </b-tooltip>
              </div>
            </div>
          </div>
        </div>
      </b-collapse>
    </div>
    <b-button type="is-dark" outlined
      expanded
      @click="clickSubmit">
      <template v-if="droppedFiles.length === 0">
        Neu
      </template>
      <template v-else>
        Vorbereiten
      </template>
    </b-button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: "MenuCreateNew",
  computed: {
    ...mapGetters('menu', ['droppedFiles', 'previewImages', 'isPreviewLoading'])
  },
  methods: {
    deleteDropFile(name) {
      // TODO: this should prolly be combined in an action
      this.$store.commit("menu_removePreviewImage", name);
      this.$store.commit("menu_removeDroppedFile", name);
    },
    clickSubmit() {
      this.$store.dispatch("menu/newProtocol");
    },
    updateDroppedFiles(e) {
      // TODO: this should prolly be combined in the action
      this.$store.commit("menu_droppedFiles", e);
      this.$store.dispatch("menu/loadPreviews");
    }
  }
}
</script>

<style>

</style>

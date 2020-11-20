<template>
  <div>
    <b-field>
      <b-upload v-model="dropFiles"
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
      <b-collapse v-show="dropFiles.length > 0" class="card" animation="slide" :open="false" aria-id="contentIdForA11y3">
        <div
          slot="trigger"
          slot-scope="props"
          class="card-header"
          role="button"
          aria-controls="contentIdForA11y3"
          :disabled="previewImages.length === 0">
          <p class="card-header-title">
            {{ dropFiles.length }} Bild(er) ausgewählt
          </p>
          <a class="card-header-icon">
            <b-icon
              :icon="props.open ? 'menu-down' : 'menu-up'">
            </b-icon>
          </a>
        </div>
        <div class="card-content" style="overflow-x: auto">
          <div class="tile is-ancestor">
            <div v-for="(img, i) in previewImages" class="tile is-parent" :key="i">

              <div class="tile is-child box">
                <b-tooltip position="is-bottom" type="is-light" always>
                  <template slot="content">
                    {{ img.name }}
                    <button class="delete is-small"
                          type="button"
                          @click="deleteDropFile(i)">
                    </button>
                  </template>
                  <figure class="image is-128x128">
                    <img :src="img.url" />
                  </figure>
                </b-tooltip>
              </div>

            </div>
          </div>
        </div>
      </b-collapse>
    </div>
    <b-button class="is-primary is-light"
      expanded
      :disabled="dropFiles.length === 0"
      @click="clickSubmit">
      Vorbereiten
    </b-button>
  </div>
</template>

<script>
export default {
  name: "MenuCreateNew",
  data() {
    return {
      dropFiles: [],
      previewImages: [],
    }
  },
  computed: {
    isPreviewLoading() {
      return this.dropFiles.length !== this.previewImages.length;
    }
  },
  watch: {
    dropFiles() {
      if (this.isPreviewLoading !== true) {
        return;
      }

      this.previewImages.splice(0, this.previewImages.length);
      this.dropFiles.forEach((file, i) => {
        const reader = new FileReader();
        reader.onload = e => {
          this.previewImages.push({
            index: i,
            name: file.name,
            url: e.target.result
          });
        };
        reader.readAsDataURL(file);
      });
    }
  },
  methods: {
    deleteDropFile(index) {
      const fi = this.previewImages[index].index;
      this.previewImages.splice(index, 1);
      this.dropFiles.splice(fi, 1);
    },
    clickSubmit(e) {
      console.log("MenuCreateNew Submit Clicked");
      console.log(e);
    }
  }
}
</script>

<style>

</style>

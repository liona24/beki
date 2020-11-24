<template>
  <div class="box">
    <status-indicator :status="base.$status">
      <a class="tag delete is-danger" slot="left" @click="removeEntry"></a>
    </status-indicator>

    <autocomplete-text :default="flaw" @update:value="updateFlaw" required>
      Mangel (flaws:flaw):
    </autocomplete-text>

    <div class="columns">
      <div class="column">
        <autocomplete-text :default="priority" @update:value="updatePriority" required>
          Priorität (flaws:priority):
        </autocomplete-text>

        <b-field label="Bemerkungen (flaws:notes):" horizontal>
          <textarea class="textarea">
            TODO: Add autocomplete
          </textarea>
        </b-field>
      </div>
      <div class="column is-one-quarter">
        <b-field v-if="!img">
          <b-upload v-model="imgFile"
              :disabled="!!imgFile"
              drag-drop>
              <section class="section">
                  <div class="content has-text-centered">
                      <p>
                          <b-icon
                              icon="upload"
                              size="is-large">
                          </b-icon>
                      </p>
                      <p>Bild hinzufügen</p>
                  </div>
              </section>
          </b-upload>
        </b-field>
        <template v-else>
          <b-tooltip position="is-bottom" type="is-light" always>
            <template slot="content">
              {{ imgFile.name }}
              <button class="delete is-small"
                    type="button"
                    @click="removeImage">
              </button>
            </template>
            <figure class="image">
              <img :src="img" />
            </figure>
          </b-tooltip>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import StatusIndicator from '../../utility/StatusIndicator'
import AutocompleteText from '../../utility/AutocompleteText'
import { mapGetters } from 'vuex'

export default {
  name: "EditorFlaw",
  components: { StatusIndicator, AutocompleteText },
  props: {
    entry: Number,
    index: Number,
  },
  data() {
    return {
      imgFile: null,
    }
  },
  computed: {
    ...mapGetters('protocol', ['entries']),
    base() {
      return this.entries[this.entry].flaws[this.index];
    },
    flaw() {
      return this.base.flaw;
    },
    priority() {
      return this.base.priority;
    },
    notes() {
      return this.base.notes;
    },
    img() {
      return this.base.img;
    }
  },
  watch: {
    imgFile() {
      // TODO: overthink the handling of images
      // we probably need the url AND the image name in the store
      // right now this assumes an url only
      // We might have to handle duplicates somehow though

      if (this.imgFile !== null) {
        const reader = new FileReader();
        reader.onload = e => {
          console.log("Image loaded", e)
          // this.imgPreviewUrl = e.target.result;
        };
        reader.readAsDataURL(this.imgFile);
      }
    }
  },
  methods: {
    removeEntry() {
      this.$store.commit("entry_removeFlaw", { entry: this.entry, i: this.index });
    },
    removeImage() {
      this.imgFile = null;
      this.$store.commit("flaw_img", { entry: this.entry, i: this.index, val: null });
    }
  }
}
</script>

<style>

</style>

<template>
  <div class="box">
    <status-indicator :status="base.$status">
      <a class="tag delete is-danger" @click="removeEntry"></a>
    </status-indicator>

    <autocomplete-text :value="title" @input="updateTitle" request-key="title" request-src="flaw" required>
      Mangel:
    </autocomplete-text>

    <div class="columns">
      <div class="column">
        <autocomplete-text :value="priority" @input="updatePriority" request-key="priority" request-src="flaw" required>
          Priorität:
        </autocomplete-text>

        <b-field label="Bemerkungen:" horizontal>
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
    title() {
      return this.base.title;
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
    },
    updateTitle(e) {
      this.$store.commit("flaw_title", { entry: this.entry, i: this.index, val: e });
    },
    updatePriority(e) {
      this.$store.commit("flaw_priority", { entry: this.entry, i: this.index, val: e });
    },
    updateNotes(e) {
      this.$store.commit("flaw_notes", { entry: this.entry, i: this.index, val: e });
    }
  }
}
</script>

<style>

</style>

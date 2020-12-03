<template>
  <div class="box">
    <status-indicator :status="base.$status">
      <a class="tag delete is-danger" @click="removeEntry"></a>
    </status-indicator>

    <div class="columns">
      <div class="column">
        <autocomplete-text :value="title" @input="updateTitle" request-key="title" request-src="flaw">
          Mangel:
        </autocomplete-text>

        <autocomplete-text :value="priority" @input="updatePriority" request-key="priority" request-src="flaw">
          Priorität:
        </autocomplete-text>

        <b-field label="Bemerkung:" horizontal>
          <autocomplete-textarea
            request-key="notes"
            request-src="flaw"
            :value="notes"
            @input="updateNotes">
          </autocomplete-textarea>
        </b-field>
      </div>
      <div class="column is-one-quarter">
        <b-field v-if="!picture">
          <b-upload v-model="imgFile"
              :disabled="!!imgFile"
              accept="image/*"
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
              {{ imgFile ? imgFile.name : '' }}
              <button class="delete is-small"
                    type="button"
                    @click="removePicture">
              </button>
            </template>
            <figure class="image">
              <img :src="pictureUrl" />
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
import AutocompleteTextarea from '../../utility/AutocompleteTextarea.vue'
import { mapGetters } from 'vuex'

export default {
  name: "EditorFlaw",
  components: { StatusIndicator, AutocompleteText, AutocompleteTextarea },
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
    picture() {
      return this.base.picture;
    },
    pictureUrl() {
      return `/images/${this.picture}`;
    }
  },
  watch: {
    imgFile() {
      if (this.imgFile === null) {
        return;
      }
      const name = this.imgFile.name;
      const onErr = () => {
        this.$buefy.snackbar.open({
          duration: 6000,
          message: `Bild '${name}' konnte nicht gespeichert werden!`,
          type: 'is-danger',
          queue: false
        });
        this.imgFile = null;
      };
      const data = new FormData();
      data.append(name, this.imgFile);
      fetch("/api/_upload", {
        method: "POST",
        body: data
      })
      .then(resp => resp.json())
      .then(json => {
        if (json[name]) {
          this.$store.commit("flaw_picture", { entry: this.entry, i: this.index, val: json[name] });
          this.imgFile = null;
        } else {
          onErr();
        }
      }, onErr)
      .catch(onErr);
    }
  },
  methods: {
    removeEntry() {
      this.$store.commit("entry_removeFlaw", { entry: this.entry, i: this.index });
    },
    removePicture() {
      this.imgFile = null;
      this.$store.commit("flaw_picture", { entry: this.entry, i: this.index, val: null });
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

<template>
  <div class="box">
    <status-indicator type="is-warning" content="Status">
      <a class="tag delete is-danger" slot="left" @click="removeEntry(0)"></a>
    </status-indicator>

    <autocomplete-input :default="flaw" @update:value="flaw = $event" required>
      Mangel (flaws:flaw):
    </autocomplete-input>

    <div class="columns">
      <div class="column">
        <autocomplete-input :default="priority" @update:value="priority = $event" required>
          Priorität (flaws:priority):
        </autocomplete-input>

        <b-field label="Bemerkungen (flaws:notes):" horizontal>
          <textarea class="textarea">
            TODO: Add autocomplete
          </textarea>
        </b-field>
      </div>
      <div class="column is-one-quarter">
        <b-field v-if="!imgFile">
          <b-upload v-model="imgFile"
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
              <img :src="imgPreviewUrl" />
            </figure>
          </b-tooltip>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import StatusIndicator from '../utility/StatusIndicator'
import AutocompleteInput from '../utility/AutocompleteInput'

export default {
  name: "EditorFlaw",
  components: { StatusIndicator, AutocompleteInput },
  data() {
    return {
      flaw: "",
      priority: "",
      notes: "",
      imgFile: null,
      imgPreviewUrl: null
    }
  },
  watch: {
    imgFile() {
      if (this.imgFile !== null) {
        const reader = new FileReader();
        reader.onload = e => {
          this.imgPreviewUrl = e.target.result;
        };
        reader.readAsDataURL(this.imgFile);
      }
    }
  },
  methods: {
    removeEntry(i) {
      console.log("Flaw remove", i);
    },
    removeImage() {
      this.imgFile = null;
      this.imgPreviewUrl = null;
    }
  }
}
</script>

<style>

</style>

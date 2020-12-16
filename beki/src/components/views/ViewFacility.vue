<template>
  <simple-editor-layout title="Einrichtung" commit-action="facility/store">
    <div class="columns">
      <div class="column is-three-quarters">
        <b-field label="Name:" horizontal>
          <b-input
              type="text"
              :value="name"
              @input="updateName"
              placeholder="Kindergarten Musterstadt"
              expand
              required>
          </b-input>
        </b-field>
        <b-field label="Straße/Nr.:" horizontal>
          <b-input
              type="text"
              :value="street"
              @input="updateStreet"
              placeholder="Musterstraße 13"
              expand>
          </b-input>
        </b-field>
        <b-field label="Postleitzahl:" horizontal>
          <b-input
              type="text"
              :value="zipCode"
              @input="updateZipCode"
              placeholder="12345"
              pattern="[0-9]{5}"
              expand>
          </b-input>
        </b-field>
        <b-field label="Stadt:" horizontal>
          <b-input
              type="text"
              :value="city"
              @input="updateCity"
              placeholder="Musterstadt"
              expand
              required>
          </b-input>
        </b-field>
      </div>
      <div class="column">
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
        <removable-image v-else :url="pictureUrl" @remove="updatePicture(null)" />
      </div>
    </div>
  </simple-editor-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import SimpleEditorLayout from '../content/editor/generic/SimpleEditorLayout.vue'
import RemovableImage from '../utility/RemovableImage.vue';

export default {
  components: { SimpleEditorLayout, RemovableImage },
  name: "ViewFacility",
  data() {
    return {
      imgFile: null
    };
  },
  computed: {
    ...mapGetters('facility', [
      'name',
      'street',
      'zipCode',
      'city',
      'picture',
    ]),
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
          this.updatePicture(json[name]);
          this.imgFile = null;
        } else {
          onErr();
        }
      }, onErr)
      .catch(onErr);
    }
  },
  methods: {
    updateName(e) {
      this.$store.commit("facility_name", e);
    },
    updateStreet(e) {
      this.$store.commit("facility_street", e);
    },
    updateZipCode(e) {
      this.$store.commit("facility_zipCode", e);
    },
    updateCity(e) {
      this.$store.commit("facility_city", e);
    },
    updatePicture(e) {
      this.$store.commit("facility_picture", e);
    }
  }
}
</script>

<style>

</style>

<template>
  <div class="box">
    <status-indicator :status="currentStatus">
      <h4 class="title is-4">{{ title }}</h4>
    </status-indicator>
    <slot>
    </slot>
    <nav class="level">
      <div class="level-left"></div>
      <div class="level-right">
        <div class="level-item">
          <button class="button is-dark" @click="commit">Speichern</button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import StatusIndicator from '../../../utility/StatusIndicator.vue'

export default {
  components: { StatusIndicator },
  name: "SimpleEditorLayout",
  props: {
    commitAction: String,
    title: String,
  },
  computed: {
    ...mapGetters(['currentStatus'])
  },
  methods: {
    commit() {
      this.$store.dispatch(this.commitAction)
        .then(wasUpdated => {
          if (wasUpdated) {
            console.log("TODO: snackbar erfolgreich gespeichert", this.title);
          }
          this.$store.commit('pop', { discard: !wasUpdated });
        }, () => {
          console.log("TODO: snackbar nicht erfolgreich gespeichert", this.title);
        });
    }
  }
}
</script>

<style>

</style>

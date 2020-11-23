<template>
  <div class="block">
    <b-field :label="label">
      <b-field>
        <b-taginput placeholder="Hinzufügen ..."
            :value="value"
            :data="data"
            :loading="isFetching"
            field="meta.repr.short"
            :required="required"
            @input="updateSelection"
            @typing="fetchData"
            attached
            expanded>
            <template slot="empty">Keine Übereinstimmung.</template>
        </b-taginput>
        <p class="control">
            <button class="button" @click="spawnEdit"><b-icon icon="pencil" ></b-icon></button>
        </p>
        <p class="control">
            <button class="button" @click="spawnCreateNew"><b-icon icon="file" ></b-icon></button>
        </p>
      </b-field>
    </b-field>

    <slot></slot>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'

export default {
  name: "CrossReferenceManySelection",
  props: {
    label: String,
    required: {
      type: Boolean,
      default: false
    },
    endpoint: String,
    value: {
      type: Array,
      default: () => {
        return [ ]
      }
    }
  },
  data() {
    return {
      isFetching: false,
      data: [
        {
          id: 1,
          meta: {
            repr: { short: "Short descr", long: "Long description" },
            is_dirty: false
          },
        }
      ]
    }
  },
  methods: {
    fetchData: debounce(function(query) {
      if (query.length === 0) {
        this.data = [];
        return;
      }

      this.isFetching = true;
      setTimeout(() => this.isFetching = false, 2000);
      /*
      this.$http.get(`https://api.themoviedb.org/3/search/movie?api_key=bb6f51bef07465653c3e553d6ab161a8&query=${name}`)
                    .then(({ data }) => {
                        this.data = []
                        data.results.forEach((item) => this.data.push(item))
                    })
                    .catch((error) => {
                        this.data = []
                        throw error
                    })
                    .finally(() => {
                        this.isFetching = false
                    })
      */
    }, 500),
    spawnEdit() {
      console.log("Edit clicked");
      this.$emit("open-modal");
    },
    spawnCreateNew() {
      console.log("Create new clicked");
      this.$emit("input", null);
      this.$emit("open-modal");
    },
    updateSelection(selection) {
      console.log("Update selection", selection);
      this.$emit("input", selection);
    }
  }
}
</script>

<style>

</style>

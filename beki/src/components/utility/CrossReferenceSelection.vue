<template>
  <div class="block">
    <b-field :label="label" horizontal>
      <b-field>
        <b-autocomplete placeholder="Suchen ..."
            v-model="innerSearchString"

            type="search"
            icon="magnify"
            field="repr"

            :data="selectable"
            :loading="isFetching"
            :required="required"
            :open-on-focus="true"

            @select="updateSelection"
            @typing="fetchData"
            @blur="makeSureSelectionIsUpdated"

            clearable
            expanded>

             <template slot="footer">
              <a @click="spawnCreateNew">
                  <span>Hinzufügen ... </span>
              </a>
            </template>

        </b-autocomplete>
        <p class="control">
            <button class="button" @click="spawnEdit" :disabled="!value"><b-icon icon="pencil" ></b-icon></button>
        </p>
        <p class="control">
            <button class="button" @click="spawnCreateNew"><b-icon icon="file" ></b-icon></button>
        </p>
      </b-field>
    </b-field>

    <slot></slot>
    <p>
      {{ selectable }}
    </p>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'

export default {
  name: "CrossReferenceSelection",
  props: {
    label: String,
    required: {
      type: Boolean,
      default: false
    },
    endpoint: String,
    value: Object,
    defaultValue: Object,
  },
  data() {
    return {
      isFetching: false,
      innerSearchString: "",
      data: [],
    }
  },
  computed: {
    selectable() {
      return this.data.map(el => {
        return {
          id: el.value.id,
          repr: el.repr()
        };
      });
    }
  },
  watch: {
    value() {
      // TODO: this may be a bad idea
      // the idea was to sync an *extern* selection
      const repr = this.value.repr();
      if (repr !== this.innerSearchString) {
        this.innerSearchString = repr;
      }
    }
  },
  methods: {
    updateSelection(e) {
      console.log("Selection changed", e);
      const val = this.data.find(el => el.value.id === e.id);
      this.$emit("input", val || this.defaultValue);
    },
    fetchData: debounce(function(query) {
      if (query.length === 0) {
        this.data = [];
        return;
      }

      this.isFetching = true;
      setTimeout(() => {
        this.isFetching = false
        this.data = this.$store.state.tmp.organizations;
      }, 500);
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
      console.log("TODO: prepare tmp state object")
      this.$emit("open-modal");
    },
    spawnCreateNew() {
      console.log("Create new clicked");
      console.log("TODO: clear tmp state object")
      this.$emit("open-modal");
    },
    makeSureSelectionIsUpdated() {
      // this method is here to check if the selection was updated
      // in the case the user *only* types the name of the element
      // he/she wishes to select without actually clicking it.
      // In this case the expected behaviour would be that the element
      // was actually selected, which we make sure of here

      const repr = this.value.value.repr();
      if (repr !== this.innerSearchString) {
        const candidate = this.selectable.find(el => el.repr === this.innerSearchString);
        if (candidate !== undefined) {
          this.updateValue(candidate);
        } else if (this.innerSelected.id !== null) {
          this.updateValue({
            repr: "",
            id: null
          });
        }
      }
    }
  }
}
</script>

<style>

</style>

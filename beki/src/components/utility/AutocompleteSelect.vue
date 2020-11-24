<template>
  <b-field :label="label" horizontal>
    <b-field>
      <b-autocomplete placeholder="Suchen ..."
        v-model="innerSearchString"

        type="search"
        icon="magnify"
        field="$repr"

        :data="data"
        :loading="isFetching"
        :required="required"
        :open-on-focus="true"

        @select="updateSelection"
        @typing="fetchData"
        @blur="makeSureSelectionIsUpdated"

        clearable
        expanded>

        <template slot="footer">
          <a @click="() => launchEditor(false)">
            <span>Hinzufügen ... </span>
          </a>
        </template>
      </b-autocomplete>
      <p class="control">
        <button class="button" @click="() => launchEditor(true)"><b-icon icon="pencil" ></b-icon></button>
      </p>
      <p class="control">
        <button class="button" @click="() => launchEditor(false)"><b-icon icon="file" ></b-icon></button>
      </p>
    </b-field>
  </b-field>
</template>

<script>
import { SyncStatus } from '../../store/common'
import { debounce, cloneDeep } from 'lodash'

export default {
  name: "AutocompleteSelect",
  props: {
    required: {
      type: Boolean,
      default: false
    },
    label: String,
    endpoint: String,
    value: Object,
  },
  data() {
    return {
      initialValue: cloneDeep(this.value),
      data: [],
      isFetching: false,
      innerSearchString: this.value.$repr
    }
  },
  methods: {
    updateSelection(e) {
      if (!e) {
        this.$emit("input", cloneDeep(this.initialValue));
      } else {
        this.$emit("input", e);
      }
    },
    fetchData: debounce(function() {
      this.isFetching = true;
      console.log("Fetching from ", this.endpoint);
      // TODO: fetch actual autocompletions
      setTimeout(() => this.isFetching = false, 500);
    }, 500),
    launchEditor(edit) {
      const obj = cloneDeep(this.value);
      if (edit !== true) {
        obj.$status = SyncStatus.New;
      }
      this.$store.commit("push", obj);
    },
    makeSureSelectionIsUpdated() {
      // this method is here to check if the selection was updated
      // in the case the user *only* types the name of the element
      // he/she wishes to select without actually clicking it.
      // In this case the expected behaviour would be that the element
      // was actually selected, which we make sure of here

      if(this.$store.getters.currentViewType === this.value.$type) {
        // blurred by entering the next view, skip
        return;
      }

      const repr = this.value.$repr;
      if (repr !== this.innerSearchString) {
        const candidate = this.data.find(el => el.$repr === this.innerSearchString);
        this.updateSelection(candidate);
      }
    }
  }

}
</script>

<style>

</style>

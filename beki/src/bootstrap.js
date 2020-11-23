import { isFunction } from 'lodash'

function _base(data, initial, repr) {
  if(initial !== null) {
    Object.keys(data).forEach(k => {
      if(initial[k] === undefined) {
        return;
      }

      if(isFunction(data[k])) {
        data[k] = data[k](initial[k]);
      } else {
        data[k] = initial[k];
      }
    });
  }

  data.$meta = {
    repr: () => repr(data)
  }

  return data
}

export function newImage(initial = null) {

}

export function newCategory(initial = null) {
  return _base({
    id: null,
    name: "",
    inspection_standards: [],
  }, initial, obj => obj.name);
}

export function newInspectionStandard(initial = null) {
  return _base({
    id: null,
    din: "",
    has_version: "Nein",
    description: ""
  }, initial, obj => obj.description);
}

export function newFlaw(initial = null) {

}

export function newEntry(initial = null) {
  return _base({
    id: null,
    category: newCategory,
    category_version: "",
    title: "",
    manufacturer: "",
    year_built: "",
    inspection_signs: "",
    manufacture_info_available: "Keine Angabe",
    easy_access: "Keine Angabe",
    flaws: []
  }, initial, obj => obj.title);
}

export function newPerson(initial = null) {
  return _base({
    id: null,
    name: "",
    first_name: "",
    email: "",
    organization: newOrganization,
  }, initial, obj => `${obj.name}, ${obj.first_name}`);
}

export function newOrganization(initial = null) {
  return _base({
    id: null,
    name: "",
    street: "",
    zip_code: "",
    city: "",
  }, initial, obj => obj.name);
}

export function newFacility(initial = null) {
  return _base({
    id: null,
    name: "",
    street: "",
    zip_code: "",
    city: "",
    img: newImage
  }, initial, obj => obj.name);
}

# Forms

Type: `content`  
Enabled by default: `true`

Specify forms in YAML syntax!

---

A sample form could look like this:
```yaml
forms:
  example:
    action: sample.php
    classes: large

    group-basic:
      legend: Basic Data
      name:
        type: text
        required: true
        placeholder: Name
      mail:
        type: email
        required: true
        placeholder: E-Mail

    topic:
      type: select
      multiple: false
      default: standard
      options:
        n1: something
        n2: standard
        n3: something else

    message:
      type: textarea
      required: true
      classes: extra
      value: Pre-filled with this

    gdpr:
      type: checkbox
      value: agreed
      label: Agree to GDPR
      name: gdpr-checkbox

    send:
      type: button
      value: Send Now
      action: submit
```

You can then display the form in your templates:
```html
{{ form_example }}
```

Forms can contain the following attributes:
```yaml
classes: extra classes
action: what to to do on submit
```

Groups can have the following attributes:
```yaml
classes: extra classes
legend: a legend for the fieldset
```

Form fields can have the following attributes:
```yaml
classes: extra classes
required: bool
label: false or label text
label-after: false or label text
type: type of input
options: needed by select, radio types
default: default value
multiple: bool (for select)
placeholder: placeholder value
rows: for textarea
cols: for textarea
```
---

|argument			|default value		|explanation									|
|-------------------|-------------------|-----------------------------------------------|
|PRIORITY			|5					|												|

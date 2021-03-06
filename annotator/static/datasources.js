"use strict";

var DataSources = {
    frame: {
        fromJson: function(json) {
            return {
                bounds: Bounds.fromAttrs({
                    x: json.x,
                    y: json.y,
                    width: json.w,
                    height: json.h,
                }),
                time: json.frame,
                continueInterpolation: json.continueInterpolation === false ? false : true,
                state: json.state,
            };
        },

        toJson: function(frame) {
            var attr = Bounds.toAttrs(frame.bounds);
            return {
                x: attr.x,
                y: attr.y,
                w: attr.width,
                h: attr.height,
                continueInterpolation: frame.continueInterpolation,
                frame: frame.time,
                state: frame.state,
            };
        },
    },

    annotation: {
        fromJson: function(json) {
            var annotation = Annotation.newFromCreationRect();
            annotation.keyframes = json.keyframes.map(DataSources.frame.fromJson);
            annotation.type = json.type;
            annotation.fill = json.color || Misc.getRandomColor();
            annotation.id = json.id;
            return annotation;
        },

        toJson: function(annotation) {
            return {
                keyframes: annotation.keyframes.map(DataSources.frame.toJson),
                type: annotation.type,
                color: annotation.fill,
                id: annotation.id,
            };
        },
    },

    annotations: {
        fromJson: function(json) {
            return json.map(DataSources.annotation.fromJson);
        },

        toJson: function(annotations) {
            return annotations.map(DataSources.annotation.toJson);
        },

        load: function(id) {
            return fetch(`/annotation/${id}`, {
                method: 'get',
                credentials: 'same-origin'
            }).then((response) => {
                if (!response.ok) {
                    return Promise.reject("DataSources.Annotations.load failed: fetch");
                }
                return response.text();
            }).then((text) => {
                var json = (text === '') ? [] : JSON.parse(text);
                var annotations = DataSources.annotations.fromJson(json);

                return Promise.resolve(annotations);
            });
        },

        save: function(id, annotations, metrics) {
            var json = DataSources.annotations.toJson(annotations);
            return fetch(`/annotation/${id}/`, {
                headers: {
                    'X-CSRFToken': window.CSRFToken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
                method: 'post',
                body: JSON.stringify({
                    annotation: json,
                    metrics: metrics,
                    assignmentId: window.assignmentId,
                }),
            }).then((response) => {
                if (response.ok) {
                    return Promise.resolve('State saved successfully.');
                } else {
                    response.text().then(t => console.log(t));
                    return Promise.resolve(`Error code ${response.status}`);
                }
            });
        },






    },
    video: {

        delete: function(ids) {
            return fetch(`/delete_video/`, {
                headers: {
                    'X-CSRFToken': window.CSRFToken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
                method: 'post',
                body: JSON.stringify({
                    ids: ids,
                }),
            }).then((response) => {
                if (response.ok) {
                    return Promise.resolve('delete videos successfully.');
                } else {
                    response.text().then(t => console.log(t));
                    return Promise.resolve(`Error code ${response.status}`);
                }
            });
        },
    },
    project: {

        delete: function(id) {
              return fetch(`/delete_project/`, {
                headers: {
                    'X-CSRFToken': window.CSRFToken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
                method: 'post',
                body: JSON.stringify({
                    project_to_be_deleted: id,
                }),
            }).then((response) => {
                if (response.ok) {
                    return Promise.resolve('delete project successfully.');
                } else {
                    response.text().then(t => console.log(t));
                    return Promise.resolve(`Error code ${response.status}`);
                }
            });
        },






    },
};

void DataSources;

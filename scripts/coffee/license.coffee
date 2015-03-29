# sic - text feedback application
#
# Copyright (C) 2015  Paul R. Tagliamonte <tag@pault.ag>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



cm = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    readOnly: true,
    mode: "htmlmixed",
    theme: "neo",
})


update = () ->
    $.getJSON({
        url: "#",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
    }, (x) ->
        cmax = Math.max.apply(null, x.comment_map.map((x) -> x.value))
        for comment in x.comment_map
            val = parseInt((comment.value / cmax) * 5)
            val = 1 if val == 0

            cm.markText({
                line: comment.start.line,
                ch: comment.start.column
            }, {
                line: comment.end.line,
                ch: comment.end.column
            }, {
                className: "heat" + val
            }))

update()


$("#comment").click(
    (e) -> 
        sections = cm.listSelections()
        text_sections = cm.getSelections()
        if sections.length != 1
            e.stopImmediatePropagation()
            return false

        text = text_sections[0]
        section = sections[0]
        head = section.head
        anchor = section.anchor

        if head.line == anchor.line && head.ch == anchor.ch
            alert("Select some text :)")
            e.stopImmediatePropagation()
            return false

        $("#quoted-text").text(text)

        $("#start_line").val(anchor.line)
        $("#end_line").val(head.line)
        $("#start_ch").val(anchor.ch)
        $("#end_ch").val(head.ch))


$("#submit-comment").click(
    (e) ->
        start_line = $("#start_line").val()
        end_line = $("#end_line").val()
        start_ch = $("#start_ch").val()
        end_ch = $("#end_ch").val()
        comment = $("#comment-text").val()
        $.post("#", {
            start_line: start_line,
            end_line: end_line,
            start_ch: start_ch,
            end_ch: end_ch,
            comment: comment,
        }, (d) ->
            update()
            $("#modal").modal('hide')
            $("#comment-text").val('')))

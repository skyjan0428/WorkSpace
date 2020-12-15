(set-option :produce-models true)
 (set-logic ALL)
(declare-fun *title () String)
(assert (str.contains (str.++ "<!DOCTYPE html PUBLIC -//W3C//DTD HTML 4.0 Transitional//EN>
<html><head><title> Python:" (+ *head *content) "</title>
<meta http-equiv=Content-Type content=text/html; charset=utf-8>
</head><body bgcolor=#f0f0f8>
<table width=100% cellspacing=0 cellpadding=2 border=0 summary=heading>
<tr bgcolor=#7799ee>
<td valign=bottom>&nbsp;<br>
<font color=#ffffff face=helvetica, arial>&nbsp;<br><big><big><strong>XML-RPC Server Documentation</strong></big></big></font></td
><td align=right valign=bottom
><font color=#ffffff face=helvetica, arial>&nbsp;</font></td></tr></table>
    <p><tt>This&nbsp;server&nbsp;exports&nbsp;the&nbsp;following&nbsp;methods&nbsp;through&nbsp;the&nbsp;XML-RPC&nbsp;protocol.</tt></p>
<p>
<table width=100% cellspacing=0 cellpadding=2 border=0 summary=section>
<tr bgcolor=#eeaa77>
<td colspan=3 valign=bottom>&nbsp;<br>
<font color=#ffffff face=helvetica, arial>
<big><strong>Methods</strong></big></font></td></tr>
<tr><td bgcolor=#eeaa77><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width=100%></td></tr></table>
</body></html>") "script")  )
(check-sat)
 (get-model)

import re
from sqlalchemy.sql import compiler
from sqlalchemy import exc
from sqlalchemy import sql
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy.sql import compiler
from sqlalchemy.sql import operators
from sqlalchemy.sql import elements


RE_DATETIME_PATTERN = r"'(?P<Y>\d{4})-(?P<M>\d{2})-(?P<D>\d{2}) (?P<H>\d{2}):(?P<m>\d{2}):(?P<s>\d{2}).(?P<ms>\d{6})'"
def _datetime_replace(matched):
    matched_dict = matched.groupdict()
    Y_ = matched_dict['Y']
    M_ = matched_dict['M']
    D_ = matched_dict['D']
    H_ = matched_dict['H']
    m_ = matched_dict['m']
    s_ = matched_dict['s']
    ms_ = matched_dict['ms']
    return "{}.{}.{}T{}:{}:{}.{}".format(Y_, M_, D_, H_, m_, s_, ms_)

RE_JOIN_AS = r"as (?P<name>\w*)__"
def _join_as_replace(matched):
    matched_dict = matched.groupdict()
    name_ = matched_dict['name']
    if name_ == "mme_inner":
        return "as {}__".format(name_)
    else:
        return "as {}".format(name_)

RE_JOIN_ON = r"(?P<name1>\w*) = (?P<name2>\w*)__"
def _join_on_replace(matched):
    matched_dict = matched.groupdict()
    name1_ = matched_dict['name1']
    name2_ = matched_dict['name2']
    if name1_ == name2_:
        return "{}".format(name1_)
    else:
        return "{} = {}__".format(name1_, name2_)

OPERATORS = {
    # binary
    operators.and_: " && ",         # sqlparse will detect "and"/"AND" and add '\n' to sql string    refine link:sqlparse.__init__.format -> ReindentFilter._next_token
    operators.or_: " || ",
    operators.add: " + ",
    operators.mul: " * ",
    operators.sub: " - ",
    operators.div: " / ",
    operators.mod: " % ",
    operators.truediv: " / ",
    operators.neg: "-",
    operators.lt: " < ",
    operators.le: " <= ",
    operators.ne: " != ",
    operators.gt: " > ",
    operators.ge: " >= ",
    operators.eq: " = ",
    operators.is_distinct_from: " IS DISTINCT FROM ",
    operators.isnot_distinct_from: " IS NOT DISTINCT FROM ",
    operators.concat_op: " || ",
    operators.match_op: " MATCH ",
    operators.notmatch_op: " NOT MATCH ",
    operators.in_op: " in ",
    operators.notin_op: " not in ",
    operators.comma_op: ", ",
    operators.from_: " from ",
    operators.as_: " as ",
    operators.is_: " IS ",
    operators.isnot: " IS NOT ",
    operators.collate: " COLLATE ",
    # unary
    operators.exists: "EXISTS ",
    operators.distinct_op: "DISTINCT ",
    operators.inv: "NOT ",
    operators.any_op: "ANY ",
    operators.all_op: "ALL ",
    # modifiers
    operators.desc_op: " desc",
    operators.asc_op: " asc",
    operators.nullsfirst_op: " NULLS FIRST",
    operators.nullslast_op: " NULLS LAST",
}

## Preparer for sql string
class DDBIdentifierPreparer(sql.compiler.IdentifierPreparer):
    def __init__(self, dialect):
        # here changed the initial_quote to "TMP_"
        super(DDBIdentifierPreparer, self).__init__(dialect, omit_schema=True, initial_quote="")

    # TODO: delete
    def format_label(self, label, name=None):
        # print("MLOG [format_label] label=", label, " name=", name)
        return self.quote(name or label.name)

    # TODO: delete
    def quote(self, ident, force=None):
        """Conditionally quote an identfier.

        The identifier is quoted if it is a reserved word, contains
        quote-necessary characters, or is an instance of
        :class:`.quoted_name` which includes ``quote`` set to ``True``.

        Subclasses can override this to provide database-dependent
        quoting behavior for identifier names.

        :param ident: string identifier
        :param force: unused

            .. deprecated:: 0.9

                The :paramref:`.IdentifierPreparer.quote.force`
                parameter is deprecated and will be removed in a future
                release.  This flag has no effect on the behavior of the
                :meth:`.IdentifierPreparer.quote` method; please refer to
                :class:`.quoted_name`.

        """
        if force is not None:
            # not using the util.deprecated_params() decorator in this
            # case because of the additional function call overhead on this
            # very performance-critical spot.
            util.warn_deprecated(
                "The IdentifierPreparer.quote.force parameter is "
                "deprecated and will be removed in a future release.  This "
                "flag has no effect on the behavior of the "
                "IdentifierPreparer.quote method; please refer to "
                "quoted_name()."
            )

        force = getattr(ident, "quote", None)

        if force is None:
            if ident in self._strings:
                return self._strings[ident]
            else:
                if self._requires_quotes(ident):
                    self._strings[ident] = self.quote_identifier(ident)
                else:
                    self._strings[ident] = ident
                return self._strings[ident]
        elif force:
            return self.quote_identifier(ident)
        else:
            return ident
        
    # TODO: delete
    def quote_identifier(self, value):
        """Quote an identifier.

        Subclasses should override this to provide database-dependent
        quoting behavior.
        """

        return (
            self.initial_quote
            + self._escape_identifier(value)
            + self.final_quote
        )

## SQLAlchemy types to DolphinDB types
class DDBTypeCompiler(compiler.GenericTypeCompiler):
    def visit_String(self, type_, **kw):
        return 'STRING'
    
    def visit_DECIMAL(self, type_, **kw):
        return 'DOUBLE'

    def visit_VARCHAR(self, type_, **kw):
        return 'STRING'

    def visit_unicode_text(self, type_, **kw):
        return 'STRING'

## SQLAlchemy SQL to DolphinDB SQL
class DDBCompiler(compiler.SQLCompiler):
    OPERATORS = OPERATORS

    ansi_bind_rules = True
    def visit_cast(self, cast, **kwargs):
        # print("cast: ", cast)
        # print(type(cast))
        # print("kwargs: ", kwargs)
        return "cast(%s, %s)" % (
            cast.clause._compiler_dispatch(self, **kwargs),
            cast.typeclause._compiler_dispatch(self, **kwargs),
        )

    def visit_label(
        self,
        label,
        add_to_result_map=None,
        within_label_clause=False,
        within_columns_clause=False,
        render_label_as_label=None,
        **kw
    ):
        # only render labels within the columns clause
        # or ORDER BY clause of a select.  dialect-specific compilers
        # can modify this behavior.
        render_label_with_as = (
            within_columns_clause and not within_label_clause
        )
        render_label_only = render_label_as_label is label
        # print("pre labelname: ", label.name, type(label))
        labelname = ""
        if render_label_only or render_label_with_as:
            if isinstance(label.name, elements._truncated_label):
                labelname = self._truncated_identifier("colident", label.name)
            else:
                labelname = label.name
        ## labelname has `(` and `)`.
        #  replace them with `TMP_`.
        if labelname.find('(')!=-1 and labelname.find(')')!=-1:
            labelname = labelname.replace('(', "TMP_")
            labelname = labelname.replace(')', "TMP_")

        # print("format_label:", label, "|", labelname)
        if render_label_with_as:
            if add_to_result_map is not None:
                add_to_result_map(
                    labelname,
                    label.name,
                    (label, labelname) + label._alt_names,
                    label.type,
                )
            # print("ffff", self.preparer.format_label(label, labelname))
            pretmp = label.element._compiler_dispatch(
                    self,
                    within_columns_clause=True,
                    within_label_clause=True,
                    **kw
                )
            tmp =  (
                pretmp
                + OPERATORS[operators.as_]
                + self.preparer.format_label(label, labelname)
            )
            ## replace keywords
            if tmp.find("AVG(") != -1:
                tmp = tmp.replace("AVG(", "avg(")
            if tmp.find("COUNT(*)") != -1:
                tmp = tmp.replace("COUNT(*)", "count(*)")
            if tmp.find("count(DISTINCT ") != -1:
                tmp = tmp.replace("count(DISTINCT ", "(tmp_->count(distinct(tmp_)))(")
            if tmp.find("__timestamp") != -1:
                return pretmp
                tmp = tmp.replace("__timestamp", pretmp)
            # print("render_label_with_as: ", tmp)
            return tmp
        elif render_label_only:

            tmp = self.preparer.format_label(label, labelname)
            # print("render_label_only: ", tmp)
            return tmp
        else:
            tmp = label.element._compiler_dispatch(
                self, within_columns_clause=False, **kw
            )
            # print("else: ", tmp)
            return tmp

    def get_render_as_alias_suffix(self, alias_name_text):
        return " as " + alias_name_text

    def group_by_clause(self, select, **kw):
        """allow dialects to customize how GROUP BY is rendered."""

        group_by = select._group_by_clause._compiler_dispatch(self, **kw)
        if group_by:
            return " group by " + group_by
        else:
            return ""

    def order_by_clause(self, select, **kw):
        """allow dialects to customize how ORDER BY is rendered."""

        order_by = select._order_by_clause._compiler_dispatch(self, **kw)
        if order_by:
            return " order by " + order_by
        else:
            return ""

    def visit_table(
        self,
        table,
        asfrom=False,
        iscrud=False,
        ashint=False,
        fromhints=None,
        use_schema=True,
        **kwargs
    ):
        if asfrom or ashint:
            effective_schema = self.preparer.schema_for_object(table)

            if use_schema and effective_schema:
                if(effective_schema=="shared_table"):
                    ret = (self.preparer.quote(table.name))
                else:
                    ret = 'loadTable("{}", "{}")'.format(effective_schema, table.name)
            else:
                ret = self.preparer.quote(table.name)
            if fromhints and table in fromhints:
                ret = self.format_from_hint_text(
                    ret, table, fromhints[table], iscrud
                )
            return ret
        else:
            return ""

    # TODO: need to complete [full join] and [outer join]
    #       and to check [join]
    def visit_join(self, join, asfrom=False, **kwargs):
        if join.full:
            return "[TODO LIST]"
        elif join.isouter:
            return "[TODO LIST]"
        else:
            str_l = join.left._compiler_dispatch(self, asfrom=True, **kwargs)
            str_r = join.right._compiler_dispatch(self, asfrom=True, **kwargs)
            str_r = re.sub(RE_JOIN_AS, _join_as_replace, str_r)
            str_e = join.onclause._compiler_dispatch(self, **kwargs)
            str_o = re.sub(RE_JOIN_ON, _join_on_replace, str_e)
            if str_e != str_o:
                return "ej((" + str_l + "), (" + str_r + "), `" + str_o + ")"
            else:
                return "ej((" + str_l + "), (" + str_r + "), `" + str_o + ", `" + str_e + ")"
    
    # not use
    # now using `top_clause` instead
    def limit_clause(self, select, **kw):
        text = ""
        # TODO: need to support group by + limit and offset has problem
        if select._limit_clause is not None:
            a = self.process(select._limit_clause, **kw)
            # print("MLOG limit process: ", a, type(a))
            text += " limit " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            if select._limit_clause is None:
                text += " limit -1"
            text += " offset " + self.process(select._offset_clause, **kw)
        return text
    
    def top_clause(self, select, **kw):
        text = " top "
        if select._limit_clause is not None and select._offset_clause is None:
            text += "0:" + self.process(select._limit_clause, **kw) + " "
        if select._limit_clause is not None and select._offset_clause is not None:
            limitnum = (int)(self.process(select._limit_clause, **kw))
            offsetnum = (int)(self.process(select._offset_clause, **kw))
            text += (str)(offsetnum) + ":" + (str)(offsetnum + limitnum) + " "
        if select._limit_clause is None and select._offset_clause is not None:
            text += self.process(select._offset_clause, **kw) + ":50000 "
        # if select._limit_clause is None and select._offset_clause is None:
        #     text += "0:50000"
        return text

    def _compose_select_body(
        self, text, select, inner_columns, froms, byfrom, kwargs
    ):
        # if (
        #     select._limit_clause is not None
        #     or select._offset_clause is not None
        # ):
            # TODO: need to support group by + limit
            # text = "select * from (" + text + ") "
        toptext = self.top_clause(select, **kwargs)
        text += ", ".join(inner_columns)
        if froms:
            text += " from "
            if select._hints:
                text += ", ".join(
                    [
                        f._compiler_dispatch(
                            self, asfrom=True, fromhints=byfrom, **kwargs
                        )
                        for f in froms
                    ]
                )
            else:
                text += ", ".join(
                    [
                        f._compiler_dispatch(self, asfrom=True, **kwargs)
                        for f in froms
                    ]
                )
        else:
            text += self.default_from()
        # print("MLOG: Start whereclause")
        if select._whereclause is not None:
            # print("**kwargs: ", kwargs)
            t = select._whereclause._compiler_dispatch(self, **kwargs)
            ## TableColumn.dttm_sql_literal "%Y-%m-%d %H:%M:%S.%f"
            t = re.sub(RE_DATETIME_PATTERN, _datetime_replace, t)
            if t:
                text += " where " + t
        # print("MLOG: End whereclause")

        if select._group_by_clause.clauses:
            text += self.group_by_clause(select, **kwargs)

        if select._having is not None:
            t = select._having._compiler_dispatch(self, **kwargs)
            if t:
                text += " having " + t

        if select._order_by_clause.clauses:
            text += self.order_by_clause(select, **kwargs)
        
        if select._for_update_arg is not None:
            text += self.for_update_clause(select, **kwargs)

        if (
            select._limit_clause is not None
            or select._offset_clause is not None
        ):
            text = "select " + toptext + " * from (" + text + ")"

        return text

    # for OPERATORS changes
    # visit_OPERATORS 
    def visit_clauselist(self, clauselist, **kw):
        sep = clauselist.operator
        if sep is None:
            sep = " "
        else:
            sep = OPERATORS[clauselist.operator]
            # print("OPERATORS: ", sep)

        text = sep.join(
            s
            for s in (
                c._compiler_dispatch(self, **kw) for c in clauselist.clauses
            )
            if s
        )
        # TODO: "insert value"
        if clauselist._tuple_values and self.dialect.tuple_in_values:
            text = "VALUES " + text
        # print("MOG: visit_clauselist: ", text)
        return text

    # for OPERATORS change
    def visit_unary(self, unary, **kw):
        if unary.operator:
            if unary.modifier:
                raise exc.CompileError(
                    "Unary expression does not support operator "
                    "and modifier simultaneously"
                )
            disp = self._get_operator_dispatch(
                unary.operator, "unary", "operator"
            )
            if disp:
                return disp(unary, unary.operator, **kw)
            else:
                return self._generate_generic_unary_operator(
                    unary, OPERATORS[unary.operator], **kw
                )
        elif unary.modifier:
            disp = self._get_operator_dispatch(
                unary.modifier, "unary", "modifier"
            )
            if disp:
                return disp(unary, unary.modifier, **kw)
            else:
                return self._generate_generic_unary_modifier(
                    unary, OPERATORS[unary.modifier], **kw
                )
        else:
            raise exc.CompileError(
                "Unary expression has no operator or modifier"
            )

    # get operators
    def visit_binary(
        self, binary, override_operator=None, eager_grouping=False, **kw
    ):

        # don't allow "? = ?" to render
        if (
            self.ansi_bind_rules
            and isinstance(binary.left, elements.BindParameter)
            and isinstance(binary.right, elements.BindParameter)
        ):
            kw["literal_binds"] = True

        operator_ = override_operator or binary.operator
        # print("MLOG: operator_: ", operator_)
        disp = self._get_operator_dispatch(operator_, "binary", None)
        if disp:
            return disp(binary, operator_, **kw)
        else:
            try:
                opstring = OPERATORS[operator_]
                # print("MLOG: opstring: ", opstring)
            except KeyError as err:
                util.raise_(
                    exc.UnsupportedCompilationError(self, operator_),
                    replace_context=err,
                )
            else:
                return self._generate_generic_binary(binary, opstring, **kw)
    
    def _generate_generic_binary(
        self, binary, opstring, eager_grouping=False, **kw
    ):

        _in_binary = kw.get("_in_binary", False)

        kw["_in_binary"] = True
        # print("---------")
        leftstr = binary.left._compiler_dispatch(
            self, eager_grouping=eager_grouping, **kw
        )
        rightstr = binary.right._compiler_dispatch(
            self, eager_grouping=eager_grouping, **kw
        )

        if opstring == OPERATORS[operators.is_]:
            if rightstr == "NULL":
                text = " isNull(" + leftstr + ")"
            else:
                text = leftstr + opstring + rightstr
        elif opstring == OPERATORS[operators.isnot]:
            if rightstr == "NULL":
                text = " !isNull(" + leftstr + ")"
            else:
                text = leftstr + opstring + rightstr
        elif opstring == OPERATORS[operators.notin_op]:
            text = "not " + leftstr + " in " + rightstr
        else:
            text = leftstr + opstring + rightstr
        # print("MLOG: generate_binary: ", text, type(binary.right))

        if _in_binary and eager_grouping:
            text = "(%s)" % text
        # print("_generate_generic_binary: ", text)
        return text
    
    def visit_like_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)

        # TODO: use ternary here, not "and"/ "or"
        return "%s like %s" % (
            binary.left._compiler_dispatch(self, **kw),
            binary.right._compiler_dispatch(self, **kw),
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape
            else ""
        )

    def visit_notlike_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)
        return "%s not like %s" % (
            binary.left._compiler_dispatch(self, **kw),
            binary.right._compiler_dispatch(self, **kw),
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape
            else ""
        )

    def visit_ilike_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)
        return "lower(%s) like lower(%s)" % (
            binary.left._compiler_dispatch(self, **kw),
            binary.right._compiler_dispatch(self, **kw)
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape
            else ""
        )
    
    def visit_notilike_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)
        return "lower(%s) not like lower(%s)" % (
            binary.left._compiler_dispatch(self, **kw),
            binary.right._compiler_dispatch(self, **kw),
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape
            else ""
        )

    def render_literal_bindparam(self, bindparam, **kw):
        value = bindparam.effective_value
        # print("type: ", bindparam.type)
        renderstr = self.render_literal_value(value, bindparam.type)
        # print("render_literal_bindparam: value: ", value, "renderstr: ", renderstr)
        return renderstr

    def visit_bindparam(
        self,
        bindparam,
        within_columns_clause=False,
        literal_binds=False,
        skip_bind_expression=False,
        **kwargs
    ):
        # print("visit_bindparam1:")
        if not skip_bind_expression:
            impl = bindparam.type.dialect_impl(self.dialect)
            if impl._has_bind_expression:
                bind_expression = impl.bind_expression(bindparam)
                return self.process(
                    bind_expression,
                    skip_bind_expression=True,
                    within_columns_clause=within_columns_clause,
                    literal_binds=literal_binds,
                    **kwargs
                )
        # print("visit_bindparam2:")
        if literal_binds or (within_columns_clause and self.ansi_bind_rules):
            if bindparam.value is None and bindparam.callable is None:
                raise exc.CompileError(
                    "Bind parameter '%s' without a "
                    "renderable value not allowed here." % bindparam.key
                )
            return self.render_literal_bindparam(
                bindparam, within_columns_clause=True, **kwargs
            )

        name = self._truncate_bindparam(bindparam)

        if name in self.binds:
            existing = self.binds[name]
            if existing is not bindparam:
                if (
                    existing.unique or bindparam.unique
                ) and not existing.proxy_set.intersection(bindparam.proxy_set):
                    raise exc.CompileError(
                        "Bind parameter '%s' conflicts with "
                        "unique bind parameter of the same name"
                        % bindparam.key
                    )
                elif existing._is_crud or bindparam._is_crud:
                    raise exc.CompileError(
                        "bindparam() name '%s' is reserved "
                        "for automatic usage in the VALUES or SET "
                        "clause of this "
                        "insert/update statement.   Please use a "
                        "name other than column name when using bindparam() "
                        "with insert() or update() (for example, 'b_%s')."
                        % (bindparam.key, bindparam.key)
                    )

        self.binds[bindparam.key] = self.binds[name] = bindparam
        # print("visit_bindparam3:")
        return self.bindparam_string(
            name, expanding=bindparam.expanding, **kwargs
        )

    def visit_select(
        self,
        select,
        asfrom=False,
        parens=True,
        fromhints=None,
        compound_index=0,
        nested_join_translation=False,
        select_wraps_for=None,
        lateral=False,
        **kwargs
    ):
        # print("here here here")
        needs_nested_translation = (
            select.use_labels
            and not nested_join_translation
            and not self.stack
            and not self.dialect.supports_right_nested_joins
        )

        if needs_nested_translation:
            transformed_select = self._transform_select_for_nested_joins(
                select
            )
            text = self.visit_select(
                transformed_select,
                asfrom=asfrom,
                parens=parens,
                fromhints=fromhints,
                compound_index=compound_index,
                nested_join_translation=True,
                **kwargs
            )

        toplevel = not self.stack
        entry = self._default_stack_entry if toplevel else self.stack[-1]

        populate_result_map = need_column_expressions = (
            toplevel
            or entry.get("need_result_map_for_compound", False)
            or entry.get("need_result_map_for_nested", False)
        )

        if compound_index > 0:
            populate_result_map = False

        # this was first proposed as part of #3372; however, it is not
        # reached in current tests and could possibly be an assertion
        # instead.
        if not populate_result_map and "add_to_result_map" in kwargs:
            del kwargs["add_to_result_map"]

        if needs_nested_translation:
            if populate_result_map:
                self._transform_result_map_for_nested_joins(
                    select, transformed_select
                )
            return text

        froms = self._setup_select_stack(select, entry, asfrom, lateral)

        column_clause_args = kwargs.copy()
        column_clause_args.update(
            {"within_label_clause": False, "within_columns_clause": False}
        )

        text = "select "  # we're off to a good start !
        # print("text01 >  ", text, select._whereclause)
        if select._hints:
            hint_text, byfrom = self._setup_select_hints(select)
            if hint_text:
                text += hint_text + " "
        else:
            byfrom = None
        # print("text02 >  ", text, select._whereclause)
        if select._prefixes:
            text += self._generate_prefixes(select, select._prefixes, **kwargs)
        # print("text03 >  ", text, select._whereclause)
        text += self.get_select_precolumns(select, **kwargs)
        # print("text04 >  ", text, select._whereclause)
        # the actual list of columns to print in the SELECT column list.
        inner_columns = [
            c
            for c in [
                self._label_select_column(
                    select,
                    column,
                    populate_result_map,
                    asfrom,
                    column_clause_args,
                    name=name,
                    need_column_expressions=need_column_expressions,
                )
                for name, column in select._columns_plus_names
            ]
            if c is not None
        ]

        if populate_result_map and select_wraps_for is not None:
            # if this select is a compiler-generated wrapper,
            # rewrite the targeted columns in the result map

            translate = dict(
                zip(
                    [name for (key, name) in select._columns_plus_names],
                    [
                        name
                        for (key, name) in select_wraps_for._columns_plus_names
                    ],
                )
            )

            self._result_columns = [
                (key, name, tuple(translate.get(o, o) for o in obj), type_)
                for key, name, obj, type_ in self._result_columns
            ]

        text = self._compose_select_body(
            text, select, inner_columns, froms, byfrom, kwargs
        )
        # print("text05 >  ", text, select._whereclause)
        if select._statement_hints:
            per_dialect = [
                ht
                for (dialect_name, ht) in select._statement_hints
                if dialect_name in ("*", self.dialect.name)
            ]
            if per_dialect:
                text += " " + self.get_statement_hint_text(per_dialect)
        # print("text06 >  ", text)
        if self.ctes and toplevel:
            text = self._render_cte_clause() + text
        # print("text07 >  ", text)
        if select._suffixes:
            text += " " + self._generate_prefixes(
                select, select._suffixes, **kwargs
            )
        # print("text08 >  ", text)
        self.stack.pop(-1)

        if (asfrom or lateral) and parens:
            return "(" + text + ")"
        else:
            return text



class DDBDDLCompiler(sql.compiler.DDLCompiler):
    pass



# class DDBExecutionContext(default.DefaultExecutionContext):
#     def fire_sequence(self, seq, type_):
#         """Get the next value from the sequence using ``gen_id()``."""

#         return self._execute_scalar(
#             "SELECT gen_id(%s, 1) FROM rdb$database"
#             % self.identifier_preparer.format_sequence(seq),
#             type_,
#         )

# class DDBExecutionContext_kinterbasdb(DDBExecutionContext):
#     @property
#     def rowcount(self):
#         if self.execution_options.get(
#             "enable_rowcount", self.dialect.enable_rowcount
#         ):
#             return self.cursor.rowcount
#         else:
#             return -1
    


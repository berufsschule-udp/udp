package com.norma_c.graph.backend.controllers;

import com.norma_c.graph.backend.services.DatabaseService;
import jakarta.annotation.Nullable;
import jakarta.persistence.TypedQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

import static com.norma_c.graph.backend.controllers.ControllersDescriptor.EVENTS_URL;
import static java.lang.String.format;
import static java.lang.String.join;
import static org.springframework.http.ResponseEntity.badRequest;
import static org.springframework.http.ResponseEntity.ok;

@RestController
@RequiredArgsConstructor
public class EventsController {
	private final DatabaseService databaseService;

	@GetMapping(EVENTS_URL)
	public ResponseEntity<List<Event>> getEvents(
		@RequestParam("off") int offset,
		@RequestParam("lim") int limit,
		@RequestParam("als") @Nullable String channelAliasFilter
	) {
		List<Filter> filters = new ArrayList<>();

		if (channelAliasFilter != null) {
			filters.add(injectChannelAliasFilter(channelAliasFilter));
		}

		TypedQuery<Event> query
			= databaseService.createNativeTypedQuery(format("""
				SELECT
					c.id AS channelId,
					c.alias AS channelAlias,
					c.unit AS channelUnit,
					c.max_value AS channelMaxValue,
					e.alarm_level AS alarmLevel,
					e.timestamp
				FROM events e
				JOIN channels c ON c.id = e.channel_id%s
				ORDER BY e.timestamp DESC
				LIMIT %s, %s""",
			getWhereClause(filters), offset, offset + limit), Event.class);

		filters.forEach(f -> query.setParameter(f.key, f.value));
		return ok(query.getResultList());
	}

	@GetMapping(EVENTS_URL + "/distinct/id")
	public ResponseEntity<List<Event>> getEventsByDistinctChannelId() {
		return ok(databaseService.createNativeTypedQuery("""
				SELECT
					c.id AS channelId,
					c.alias AS channelAlias,
					c.unit AS channelUnit,
					c.max_value AS channelMaxValue,
					e.alarm_level AS alarmLevel,
					e.timestamp
				FROM events e
				JOIN (
					SELECT channel_id, MAX(timestamp) AS timestamp
					FROM events GROUP BY channel_id
				) l ON l.channel_id = e.channel_id
					AND l.timestamp = e.timestamp
				JOIN channels c ON c.id = e.channel_id
				ORDER BY e.timestamp DESC""", Event.class)
			.getResultList()
		);
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<String> handleException(Exception exception) {
		return badRequest().body(exception.getMessage());
	}

	private Filter injectChannelAliasFilter(String channelIdFilter) {
		return new Filter(
			format("c.alias %s :channelAlias",
				injectOperator(channelIdFilter.charAt(0))),
			"channelAlias",
			channelIdFilter.substring(1)
		);
	}

	private String injectOperator(char operator) {
		return switch (operator) {
			case '0' -> "=";
			case '1' -> "!=";
			default -> throw new IllegalArgumentException(
				"Not SQL-Safe operator: " + operator
			);
		};
	}

	private String getWhereClause(List<Filter> filters) {
		return filters.isEmpty() ? "" : "\nWHERE "
			+ join(" AND ", filters.stream().map(Filter::clause).toList());
	}

	public record Event(
		String channelId,
		String channelAlias,
		String channelUnit,
		@Nullable Double channelMaxValue,
		short alarmLevel,
		Timestamp timestamp
	) {}

	private record Filter(String clause, String key, Object value) {}
}
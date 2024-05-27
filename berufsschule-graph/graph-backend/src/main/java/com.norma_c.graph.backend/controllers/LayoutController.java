package com.norma_c.graph.backend.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.norma_c.graph.backend.services.DatabaseService;
import jakarta.annotation.Nullable;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

import static com.norma_c.graph.backend.controllers.ControllersDescriptor.LAYOUT_URL;
import static java.util.stream.Collectors.*;
import static org.springframework.http.ResponseEntity.badRequest;
import static org.springframework.http.ResponseEntity.ok;

@RestController
@RequiredArgsConstructor
public class LayoutController {
	private final DatabaseService databaseService;
	private final ObjectMapper mapper;

	@GetMapping(LAYOUT_URL)
	public ResponseEntity<Map<Short, List<Channel>>> getLayout() {
		return ok(databaseService.createNativeTypedQuery("""
				SELECT c.id, c.alias, c.unit,
					al.alarm_level AS alarmLevel, l.page AS pageIndex,
					l.offset, l.span, a.value AS lastValue
				FROM averages a
				JOIN layout l ON a.channel_id = l.channel_id
				JOIN channels c ON a.channel_id = c.id
				LEFT JOIN (
					SELECT channel_id, alarm_level
					FROM events LATEST
					ON timestamp PARTITION BY channel_id
				) al ON a.channel_id = al.channel_id
				LATEST ON timestamp PARTITION BY channel_id
				ORDER BY offset""", ChannelWithPageIndex.class)
			.getResultStream()
			.collect(groupingBy(
				ChannelWithPageIndex::pageIndex,
				mapping(c -> mapper.convertValue(c, Channel.class), toList())
			))
		);
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<String> handleException(Exception exception) {
		return badRequest().body(exception.getMessage());
	}

	private record ChannelWithPageIndex(
		String id,
		String alias,
		String unit,
		short alarmLevel,
		short pageIndex,
		short offset,
		short span,
		@Nullable Double lastValue
	) {}

	public record Channel(
		String id,
		String alias,
		String unit,
		short alarmLevel,
		short offset,
		short span,
		@Nullable Double lastValue
	) {}
}